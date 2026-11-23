"""KED Google Search Console MCP server.

One OAuth client owned by chris@kedinterests.com, one refresh token. run-mcp.sh
loads credentials from .env in this folder before exec'ing this file.

Scope is webmasters (read/write) so sitemaps can be submitted from chat.
Request Indexing has no public API and still has to be done in the Search
Console UI. The same OAuth grant also carries analytics.readonly, which
get_token.py writes to ga-adc.json for the google-analytics-ked server.

Smoke test:  ./run-mcp.sh --ping
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

REQUIRED_ENV = ["GSC_CLIENT_ID", "GSC_CLIENT_SECRET", "GSC_REFRESH_TOKEN"]
TOKEN_URI = "https://oauth2.googleapis.com/token"


def _missing_env() -> list[str]:
    return [k for k in REQUIRED_ENV if not os.environ.get(k)]


def _credentials() -> Credentials:
    missing = _missing_env()
    if missing:
        raise RuntimeError(
            f"Missing {missing}. Copy .env.example to .env, fill the client id/secret, "
            "then run get_token.py. See SETUP.md."
        )
    # No scopes on a refresh grant: the access token carries whatever was
    # consented at get_token.py time, and passing a narrower set here makes
    # Google reject the refresh with invalid_scope.
    return Credentials(
        None,
        refresh_token=os.environ["GSC_REFRESH_TOKEN"],
        client_id=os.environ["GSC_CLIENT_ID"],
        client_secret=os.environ["GSC_CLIENT_SECRET"],
        token_uri=TOKEN_URI,
    )


def _service():
    return build("searchconsole", "v1", credentials=_credentials(), cache_discovery=False)


def _call(fn) -> dict[str, Any]:
    try:
        return fn()
    except HttpError as e:
        detail = e.content.decode() if isinstance(e.content, bytes) else str(e.content)
        return {"error": f"HTTP {e.resp.status}", "detail": detail}
    except Exception as e:  # noqa: BLE001
        return {"error": type(e).__name__, "detail": str(e)}


def ping() -> dict[str, Any]:
    def go():
        sites = _service().sites().list().execute().get("siteEntry", [])
        return {
            "ok": True,
            "account": "chris@kedinterests.com",
            "site_count": len(sites),
            "sites": [s["siteUrl"] for s in sites],
        }

    return _call(go)


def list_sites() -> dict[str, Any]:
    def go():
        sites = _service().sites().list().execute().get("siteEntry", [])
        return {
            "site_count": len(sites),
            "sites": [
                {"site_url": s["siteUrl"], "permission_level": s.get("permissionLevel")}
                for s in sites
            ],
        }

    return _call(go)


def search_analytics(
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: list[str] | None = None,
    row_limit: int = 100,
    search_type: str = "web",
    page_filter: str | None = None,
    query_filter: str | None = None,
) -> dict[str, Any]:
    dims = dimensions or ["query"]
    body: dict[str, Any] = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dims,
        "rowLimit": max(1, min(int(row_limit), 25000)),
        "type": search_type,
    }
    filters = []
    if page_filter:
        filters.append({"dimension": "page", "operator": "contains", "expression": page_filter})
    if query_filter:
        filters.append({"dimension": "query", "operator": "contains", "expression": query_filter})
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]

    def go():
        res = _service().searchanalytics().query(siteUrl=site_url, body=body).execute()
        rows = []
        for r in res.get("rows", []):
            row = dict(zip(dims, r.get("keys", [])))
            row.update(
                clicks=r.get("clicks", 0),
                impressions=r.get("impressions", 0),
                ctr=round(r.get("ctr", 0.0), 4),
                position=round(r.get("position", 0.0), 1),
            )
            rows.append(row)
        return {"site_url": site_url, "start_date": start_date, "end_date": end_date, "dimensions": dims, "row_count": len(rows), "rows": rows}

    return _call(go)


def inspect_url(site_url: str, url: str) -> dict[str, Any]:
    def go():
        res = (
            _service()
            .urlInspection()
            .index()
            .inspect(body={"inspectionUrl": url, "siteUrl": site_url})
            .execute()
        )
        r = res.get("inspectionResult", {})
        idx = r.get("indexStatusResult", {})
        return {
            "url": url,
            "verdict": idx.get("verdict"),
            "coverage_state": idx.get("coverageState"),
            "indexing_state": idx.get("indexingState"),
            "robots_txt_state": idx.get("robotsTxtState"),
            "page_fetch_state": idx.get("pageFetchState"),
            "last_crawl_time": idx.get("lastCrawlTime"),
            "google_canonical": idx.get("googleCanonical"),
            "user_canonical": idx.get("userCanonical"),
            "crawled_as": idx.get("crawledAs"),
            "inspection_result_link": r.get("inspectionResultLink"),
        }

    return _call(go)


def list_sitemaps(site_url: str) -> dict[str, Any]:
    def go():
        res = _service().sitemaps().list(siteUrl=site_url).execute()
        return {"site_url": site_url, "sitemaps": res.get("sitemap", [])}

    return _call(go)


def submit_sitemap(site_url: str, feedpath: str) -> dict[str, Any]:
    def go():
        _service().sitemaps().submit(siteUrl=site_url, feedpath=feedpath).execute()
        return {"ok": True, "site_url": site_url, "submitted": feedpath}

    return _call(go)


def serve() -> None:
    from mcp.server.mcpserver import MCPServer

    mcp = MCPServer("ked-search-console")

    mcp.tool(description="Verify credentials and list the Search Console properties chris@kedinterests.com can see.")(ping)
    mcp.tool(description="List Search Console properties with permission level. Use these site_url values for the other tools.")(list_sites)
    mcp.tool(
        description=(
            "Search performance rows (clicks, impressions, ctr, position) for a property over a date range "
            "(YYYY-MM-DD). dimensions: any of query, page, country, device, date, searchAppearance. "
            "page_filter / query_filter are 'contains' substrings."
        )
    )(search_analytics)
    mcp.tool(description="Google's index status for one URL: verdict, coverage state, last crawl, canonical.")(inspect_url)
    mcp.tool(description="Sitemaps submitted for a property, with last-read and error counts.")(list_sitemaps)
    mcp.tool(description="Submit (or resubmit) a sitemap URL for a property.")(submit_sitemap)

    mcp.run()


if __name__ == "__main__":
    if "--ping" in sys.argv:
        print(json.dumps(ping(), indent=2))
        sys.exit(0)
    serve()

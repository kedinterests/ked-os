# Setup: KED Search Console + Analytics connectors

Gives Claude read/write Search Console and read-only GA4 access for every
property chris@kedinterests.com can see (mineralwise.com and the rest).

Three parts: one Google Cloud OAuth client, one browser login, one register
script. About 15 minutes, nearly all of it in the Cloud console.

## 1. Google Cloud OAuth client (once)

Signed in as **chris@kedinterests.com**:

1. https://console.cloud.google.com, create a project. Name it
   `ked-connectors`. Note the **Project ID** (not the name).
2. **APIs & Services, Library**: enable all three:
   - Google Search Console API
   - Google Analytics Data API
   - Google Analytics Admin API
3. **APIs & Services, OAuth consent screen**:
   - If kedinterests.com is a Google Workspace org, pick **Internal**. Done.
   - Otherwise pick **External**, then under **Audience / Test users** add
     `chris@kedinterests.com`. Leave it in Testing; nothing needs publishing.
4. **APIs & Services, Credentials, Create credentials, OAuth client ID**:
   - Application type **Desktop app**, name `KED Claude connectors`.
   - Copy the **Client ID** and **Client secret**.

## 2. Local credentials and the one login

```bash
cd ~/os-systems/ked-os/integrations/gsc-mcp
cp .env.example .env
chmod 600 .env
```

Open `.env` and paste in `GSC_CLIENT_ID`, `GSC_CLIENT_SECRET`, and
`GOOGLE_PROJECT_ID`. Then:

```bash
cd ~/os-systems/ked-os/integrations/gsc-mcp && .venv/bin/python get_token.py
```

A browser opens. Sign in as chris@kedinterests.com and approve both scopes.
The script writes the refresh token into `.env` and `ga-adc.json`.

Smoke test:

```bash
cd ~/os-systems/ked-os/integrations/gsc-mcp && ./run-mcp.sh --ping
```

Expect `"ok": true` and a list that includes mineralwise.com.

## 3. Register with Claude Code

```bash
cd ~/os-systems/ked-os/integrations/gsc-mcp && ./register.sh
```

Restart the Claude session. Two new servers appear:
`google-search-console-ked` and `google-analytics-ked`.

## Notes

- Scope is `webmasters` (read/write) plus `analytics.readonly`. Sitemaps can
  be submitted from chat. **Request Indexing has no public API**; that step
  stays manual in the Search Console UI.
- If the consent screen is External and left in Testing, Google expires the
  refresh token after 7 days. Either publish the app (no verification needed
  for these scopes on your own account) or use Internal.
- Secrets live only in `.env` and `ga-adc.json`, both gitignored and mode 600.

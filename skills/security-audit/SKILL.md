# Skill — Security Audit (BWW Standard)

This skill performs a structured security evaluation of code, configuration, architecture, integrations, or planned changes for BWW-managed WordPress sites.

It identifies vulnerabilities, exposure risks, and misconfigurations while ensuring compatibility with Brilliant OS and the BWW Standard Stack & Platform Assumptions.

This skill does not implement fixes unless explicitly requested. It evaluates risk and recommends mitigations.

---

## Purpose

- Detect security risks before deployment
- Prevent data exposure and compromise
- Evaluate attack surface changes
- Verify secure handling of user input and sensitive data
- Ensure compatibility with existing protections
- Provide actionable remediation guidance
- Support incident prevention and investigation

---

## When to use this skill

Use when reviewing:

- New code or features
- Plugin installations or updates
- Integrations with external services
- Forms collecting user data
- Authentication or permission changes
- File upload functionality
- API endpoints or webhooks
- Infrastructure or DNS changes
- Migration plans
- Suspected vulnerabilities
- Post-incident assessments
- Any Medium-or-higher risk change

---

## Required inputs

Before performing the audit, gather:

1. Scope of the change or system under review
2. Relevant code, configuration, or documentation
3. Data types handled (personal, financial, credentials, etc.)
4. User roles involved
5. External services or integrations
6. Exposure level (public-facing, admin-only, internal)
7. Environment details if relevant
8. Known constraints or assumptions

If critical information is missing, note uncertainty in the assessment.

---

## Audit methodology

Evaluate risk across multiple dimensions rather than focusing on a single vulnerability class.

---

## Input handling review

Assess whether all external input is treated as untrusted:

- Form submissions
- URL parameters
- Cookies
- Headers
- Uploaded files
- Imported data
- API payloads
- Admin-entered content from non-technical users

Verify:

- Validation appropriate to expected format
- Sanitization before storage
- Escaping before output
- Protection against injection attacks

---

## Authentication and authorization review

Confirm:

- Capability checks enforce privilege boundaries
- Sensitive actions require authentication
- Nonces protect state-changing requests
- Role permissions are not overly broad
- Password reset mechanisms are not exposed to abuse
- Session handling is not weakened
- Unauthorized access paths do not exist

---

## Data protection review

Identify how sensitive data is handled:

- Storage location (database, files, external services)
- Encryption where appropriate
- Exposure through logs or exports
- Inclusion in URLs or client-visible output
- Backup exposure risks
- Retention policies

Flag unnecessary collection or storage of sensitive data.

---

## File handling review

If files are accepted or generated:

- Allowed types restricted appropriately
- Executable files blocked
- Storage location not publicly executable when possible
- Access controls enforced
- Size limits applied
- Path traversal protections present
- Malware scanning compatibility maintained

---

## Integration and API review

For external connections:

- HTTPS enforced
- Credentials stored securely
- API keys not exposed in client-side code
- Incoming data validated
- Webhook authenticity verified if supported
- Rate limiting or abuse protections considered
- Failure handling does not expose sensitive details

---

## Configuration review

Identify insecure settings such as:

- Debug mode enabled in production
- Verbose error output exposed
- Weak file permissions
- Publicly accessible sensitive endpoints
- Default credentials
- Open administrative interfaces
- Unrestricted API access
- Disabled security protections

---

## Plugin and dependency risk review

Evaluate third-party components for:

- Active maintenance
- Known vulnerabilities
- Vendor reputation
- Scope of permissions required
- Potential conflicts with existing protections
- Necessity versus added attack surface

Prefer fewer, well-supported components.

---

## Attack surface analysis

Determine whether the change introduces:

- New public endpoints
- New authentication paths
- Increased exposure of data
- New privileged operations
- Automation abuse opportunities
- Cross-system trust relationships

Minimize expansion unless justified.

---

## Compatibility with BWW Standard Stack

Assess how the change interacts with protections defined in the BWW Standard Stack:

- Does it bypass or weaken existing safeguards?
- Does it duplicate security functions unnecessarily?
- Could it conflict with monitoring or firewall rules?
- Does it rely on disabling protections to function?

Flag any incompatibilities.

---

## Logging and monitoring review

Ensure security-relevant events:

- Are logged appropriately
- Do not expose sensitive data
- Can be used for incident investigation
- Will trigger alerts when necessary
- Preserve evidence integrity

---

## Common vulnerability categories to check

Evaluate for risk of:

- Cross-site scripting (XSS)
- SQL injection
- Cross-site request forgery (CSRF)
- Privilege escalation
- Authentication bypass
- File upload exploitation
- Information disclosure
- Open redirects
- Remote code execution
- Denial-of-service conditions

---

## Risk classification

Assign an overall severity:

### Low

Minimal exposure, well-contained, easily reversible.

---

### Medium

Potential impact to important functionality or limited data exposure. Requires mitigation or careful deployment.

---

### High

Affects authentication, sensitive data, or system integrity. Must be addressed before deployment.

---

### Critical

Immediate risk of compromise, data breach, or service disruption. Requires incident response.

---

## Mitigation guidance

For each identified risk:

- Explain why it is risky
- Recommend safer alternatives
- Suggest compensating controls if removal is not feasible
- Prioritize fixes by impact

Avoid vague recommendations.

---

## Output format

Provide a structured assessment:

1. Scope of review
2. Key findings
3. Identified vulnerabilities or risks
4. Attack scenarios to consider
5. Compatibility with existing protections
6. Recommended mitigations
7. Residual risk after mitigation
8. Overall risk classification
9. Approval recommendation (approve, approve with safeguards, do not approve)

---

## Incident-related usage

If auditing after a suspected compromise:

- Focus on containment and exposure
- Identify likely entry vectors
- Preserve evidence
- Avoid destructive remediation steps before analysis
- Recommend post-incident hardening

---

## Safe defaults when uncertain

- Favor the more secure interpretation
- Flag unknowns explicitly
- Recommend staged rollout when risk exists
- Escalate to Security Reviewer for complex issues
- Avoid approving changes with unverified impact on sensitive data

---

## Definition of success

This skill succeeds when:

- Security risks are identified before exploitation
- Sensitive data is adequately protected
- Recommendations are actionable and prioritized
- Compatibility with the BWW Standard Stack is maintained
- Residual risk is clearly understood
- Decision-makers can proceed with confidence
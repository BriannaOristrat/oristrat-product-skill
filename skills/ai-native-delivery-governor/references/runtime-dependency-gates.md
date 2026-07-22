# Runtime Dependency Gates

This is a foundation capability automatically inherited by delivery, UI/UX, testing, or other application work that needs a running environment. It is not a peer application or an ordinary standalone shortcut.

Use for start/stop/restart, port changes, `Failed to fetch`, proxy failures, or end-to-end acceptance.

## Layered Verification

| Layer | Evidence | What it proves |
|---|---|---|
| Process | Listener, PID, command/owner, log | Expected process owns the expected port |
| Frontend | User-facing route and static assets | Browser-facing application is reachable |
| Proxy/API route | Route response and network trace | Frontend server can route the request |
| Backend | Direct health/contract probe | Required upstream service is reachable |
| Business | Response success/code/message/data | Business validation or operation result |
| End to end | Follow-up login/readback/state change | Requested user outcome actually occurred |

HTTP `200` with business `success:false` passes route reachability only. A password-reset request with invalid parameters does not prove that a valid code resets the password.

## Failed To Fetch Diagnosis

Before editing code, inspect in this order:

1. Browser network request URL, method, payload, and console error.
2. Frontend listener and route existence.
3. proxy/base URL/environment configuration.
4. backend listener and health endpoint.
5. CORS, TLS, DNS, cookie/session, timeout, and response parsing.

Change code only after evidence identifies an implementation defect or the user authorizes an intentional fallback.

## Port Safety

- Inspect process ownership before stopping a listener.
- Stop only the explicitly scoped service/PID.
- Start hidden background services unless the user asks for an interactive window.
- Poll readiness with a bounded timeout and retain stdout/stderr logs.
- Verify old port absent and new port present after a port migration.

## Status

- `PASS`: required layers including the requested business outcome pass.
- `PARTIAL`: process/route works but backend or business success is unverified.
- `FAIL`: an expected layer returns an incorrect result.
- `BLOCKED`: access, account, valid test data, dependency, or permission prevents the required proof.

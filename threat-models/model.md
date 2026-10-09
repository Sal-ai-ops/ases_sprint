# Threat Model Dossier: nGOT Clinical & Engineering Assistant Stack

## 1. Data-Flow Diagram (DFD) & Boundaries
- **External Entity:** User (Submits natural language queries)
- **Process A (Orchestrator):** Validates session, formats system prompt, initiates model generation.
- **Data Store A (Vector Store):** Embeddings repository storing ingested PDF reports and scraped documentation.
- **Process B (Context Window / Model):** Concatenates System Prompt + User Query + Retrieved RAG Chunks + Tool Output.
- **Process C (Tool Runtime):** Executes file reads, web requests, and local database queries.
- **Boundary A (Trust Boundary):** Between external untrusted user input and application orchestrator.
- **Boundary B (Trust Boundary):** Between isolated model runtime and external downstream tools/APIs.

---

## 2. STRIDE Threat Matrix (25 Scenarios)

| ID | STRIDE Category | Target Component | Threat Scenario | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| T1 | Spoofing | User Gateway | Impersonation of high-privilege operator token | High | Mandatory OAuth2 + MFA token validation | Red Team Lead | Active |
| T2 | Spoofing | Downstream API | Agent spoofing administrative user identity to internal microservices | Critical | Issue short-lived, scoped agent-bound tokens | Blue Team Lead | Active |
| T3 | Spoofing | Tool Runtime | Malicious local process impersonating the legitimate tool execution broker | High | Mutual TLS / Unix domain socket permission checks | Tooling Lead | Active |
| T4 | Tampering | Vector Store | Direct database manipulation inserting poisoned RAG documents | High | Immutable storage write permissions + RBAC | Blue Team Lead | Active |
| T5 | Tampering | Model Weights | Unauthorized modification of local model weights on disk | Critical | Load-time SHA-256 digest verification in manifest | Tooling Lead | Active |
| T6 | Tampering | Context Window | Indirect Prompt Injection altering system prompt instructions | Critical | Strict output parsing + separate system context | Blue Team Lead | Active |
| T7 | Tampering | Ingestion Pipeline | Adversary modifies scraped web text before embedding generation | Medium | SHA-256 hash checking on raw scraped source files | Scribe | Active |
| T8 | Tampering | System Prompt | Inflight alteration of system instructions in application memory | Critical | Read-only memory allocation for system prompts | Blue Team Lead | Active |
| T9 | Repudiation | Tool Runtime | Agent executes destructive file deletion without generating audit log | High | Append-only structured JSON trace logging | Scribe | Active |
| T10 | Repudiation | Orchestrator | User denies submitting a malicious query executed by the agent | Medium | Cryptographically signed user request logs | Scribe | Active |
| T11 | Repudiation | Model Hub | Inability to prove which model version generated an invalid action | Medium | Log exact model digest alongside every invocation | Tooling Lead | Active |
| T12 | Repudiation | Vector Store | Inability to trace which retrieved document caused goal corruption | High | Record vector chunk IDs in generation metadata | Scribe | Active |
| T13 | Info Disclosure | Context Window | System prompt leakage revealing internal system secrets | Medium | Redact system prompt text from user outputs | Blue Team Lead | Active |
| T14 | Info Disclosure | Model Weights | Training data extraction extracting sensitive credentials | High | Automated canary string audits prior to release | Research Lead | Active |
| T15 | Info Disclosure | Egress Channel | Exfiltration of user secrets via malicious markdown image links | High | Restrict rendering of unverified remote image URLs | Blue Team Lead | Active |
| T16 | Info Disclosure | Vector Store | Tenant cross-contamination via unsegregated embedding queries | Critical | Enforce strict per-tenant metadata filtering | Blue Team Lead | Active |
| T17 | Info Disclosure | Error Handler | Verbose stack trace revealing internal network topology | Low | Generic public error messages + internal logging | Tooling Lead | Active |
| T18 | Denial of Service | Context Window | Unbounded context stuffing causing extreme API latency and cost | High | Enforce strict token-length limits per request | Blue Team Lead | Active |
| T19 | Denial of Service | Tool Runtime | Recursive agent loop generating infinite sub-queries | High | Set hard maximum recursion depth (max 5 turns) | Tooling Lead | Active |
| T20 | Denial of Service | Vector Store | Embedding database overload via massive document batching | Medium | Rate-limiting ingestion API endpoints | Tooling Lead | Active |
| T21 | Denial of Service | API Gateway | Exhaustion of host memory via parallel unthrottled agent streams | High | Global concurrency limiters on worker nodes | Tooling Lead | Active |
| T22 | Elevation of Priv | Tool Runtime | Agent reading local files via path traversal in tool parameters | Critical | Path sanitization + sandbox execution root | Blue Team Lead | Active |
| T23 | Elevation of Priv | Downstream API | Tool invocation beyond user's actual system permissions | Critical | Enforce user-context permission pass-through | Blue Team Lead | Active |
| T24 | Elevation of Priv | Environment | Container escape via privileged Docker execution | Critical | Run as non-root user `ases` without `--privileged` | Tooling Lead | Active |
| T25 | Elevation of Priv | Tool Registry | Dynamic registration of untrusted remote tool definitions | High | Enforce static compile-time tool allowlists | Blue Team Lead | Active |

---

## 3. Five Agentic Security Questions
1. **Provenance:** Every tool action logs `request_id`, `user_id`, and `retrieved_chunk_ids` to guarantee auditability.
2. **Reversibility:** File deletion, external HTTP POSTs, and database writes require explicit human approval gates.
3. **Blast Radius:** If the planner is compromised, it is strictly restricted to non-root `/home/ases` execution and allowlisted outbound proxy domains.
4. **Rate:** Agents are hard-limited to a maximum of 5 autonomous steps per user turn.
5. **Composition Risk:** Pairing `Read File` with `Send HTTP Request` creates an exfiltration vector; egress allowlisting mitigates this combination.

---

## 4. Accepted Risk Register
| Threat ID | Rationale for Acceptance | Review Date | Owner |
|---|---|---|---|
| T13 | System prompt details may leak via sophisticated jailbreaks; core security relies on backend tool boundaries rather than prompt secrecy. | 2026-11-01 | Blue Team Lead |
| T18 | Processing oversized medical PDFs may hit token budget limits; accepted for specialized research workflows with manual spend monitoring. | 2026-11-01 | Research Lead |
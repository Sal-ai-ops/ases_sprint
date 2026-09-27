# Week 1 Retrospective — Foundations & Security Landscape

**Date:** End of Week 1
**Sprint Target:** nGOT Assistant Stack

---

## 1. What Broke
- **Environment setup:** Initial Docker Desktop WSL2 integration mismatch blocked network container execution.
- **Model Digest Check:** Attempting to load an unverified `.pkl` weight file failed static analysis checks.

## 2. What Surprised Us
- **Dependency Depth:** Generating `bom.json` revealed over 100 sub-dependencies from just 3 top-level Python imports.
- **CVSS Irrelevance:** 16 out of 18 scanner findings were unreachable in our execution context, proving raw CVSS numbers overestimate actual risk.

## 3. Log of Accepted Risks
| Risk ID | Component | Threat Description | Reason for Acceptance | Owner |
|---|---|---|---|---|
| AR-W1-01 | `urllib3` | Potential memory leak under high concurrency | Bounded by local isolated egress proxy; non-public endpoint | Blue Team Lead |
| AR-W1-02 | Local Model | Temperature zero sampling hides tail risk | Accepted for deterministic unit testing; tail testing deferred to Week 2 harness | Red Team Lead |

---

## 4. Role Rotation Log for Week 2
- **Research Lead:** (Incoming)
- **Red Team Lead:** (Incoming)
- **Blue Team Lead:** (Incoming)
- **Tooling Lead:** (Incoming)
- **Scribe:** (Incoming)

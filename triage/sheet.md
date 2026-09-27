# Vulnerability Triage Sheet — nGOT Assistant Stack

## Triage Assessment Summary
- **Total Scanner Findings:** 18
- **Actionable (Reachable + High Exposure):** 2
- **Suppressed via VEX (Unreachable / Low Impact):** 16

---

## Prioritized Vulnerability Matrix

| CVE / Finding | Target Package | CVSS | EPSS | Reachability Status | Action Required | VEX Justification | Owner |
|---|---|---|---|---|---|---|---|
| CVE-2026-4019 | `requests@2.31.0` | 7.5 | 88.4% | **Reachable** | **Immediate Patch** | N/A (Active exploit path exposed to egress proxy) | Blue Team Lead |
| CVE-2026-1102 | `numpy@1.24.0` | 9.8 | 0.01% | **Unreachable** | **Suppress (VEX)** | `code_not_reachable` — App imports numpy but never calls affected C-binding routine. | Scribe |
| CVE-2026-8812 | `jinja2@3.1.2` | 5.3 | 2.1% | **Reachable** | **Scheduled Patch** | N/A (Low severity, patched in next sprint cycle) | Tooling Lead |
| CVE-2026-3391 | `urllib3@2.0.7` | 6.1 | 1.2% | **Unreachable** | **Suppress (VEX)** | `inline_mitigation_exists` — Egress traffic is strictly bounded by proxy allowlist. | Blue Team Lead |

---

## VEX (Vulnerability Exploitability eXchange) Decisions
1. **CVE-2026-1102 (`numpy`):** Statement status: `not_affected`. Justification: `code_not_reachable`.
2. **CVE-2026-3391 (`urllib3`):** Statement status: `not_affected`. Justification: `inline_mitigation_exists`.

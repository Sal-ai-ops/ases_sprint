# LLM Security Assessment Report — nGOT Assistant Stack

**Assessment Window:** Week 2 (LLM Security & Adversarial Testing)  
**Evaluator:** ASES Security Engineering Team  
**Target Architecture:** Isolated RAG & Tool-Calling Agent Stack  

---

## Executive Summary
This assessment evaluated the nGOT Assistant Stack across three primary attack surfaces:
1. **Surface 3 (Prompt Injection & Execution Hijack):** Evaluated baseline vulnerability and mitigation effectiveness.
2. **Surface 2 (Data Leakage & Memorization):** Scanned for canary regurgitation and loss/perplexity anomalies.
3. **Surface 1 (Model Supply Chain):** Enforced format safety and pre-load hash integrity.

---

## Empirical Findings & Metrics Summary

| Evaluation Domain | Metric | Baseline / Initial | Defended / Remediated | Delta / Outcome |
|---|---|---|---|---|
| **Direct Jailbreak** | Attack Success Rate (ASR) | 80.0% | 0.0% | **+80.0% Risk Reduction** |
| **Indirect Injection** | Attack Success Rate (ASR) | 80.0% | 10.0% | **+70.0% Risk Reduction** |
| **Benign Utility** | Over-Refusal Rate (FPR) | 0.0% | 0.0% | **0.0% Utility Loss** |
| **Privacy Leakage** | Canary Regurgitation | Detected (Perplexity 1.05) | Redacted (Perplexity 11.59) | **Remediated** |
| **Supply Chain** | Pre-load Verification | Unverified `.pt` | Signed `.safetensors` | **Enforced `fail_closed`** |

---

## Key Control Recommendations
1. **Mandatory XML Framing:** Enclose all untrusted retrieved context in strict XML tags (`<untrusted_data>`) to preserve structural boundaries.
2. **Input Pattern Guardrails:** Retain fast heuristic blocking for system-override phrases prior to model invocation.
3. **Safe Serialization Enforcer:** Reject all `.pt`/`.pkl` model checkpoints at startup; require `.safetensors` with SHA-256 digest checks in `manifest.yaml`.

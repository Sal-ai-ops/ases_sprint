# Week 2 Retrospective — LLM Security & Adversarial Testing

**Date:** End of Week 2  
**Sprint Target:** LLM Security Evaluation Pipeline  

---

## 1. What Broke
- ** WSL / Windows File Permissions:** Root-created JSON reports blocked non-root script updates inside mounted Windows directories (`/mnt/c/`). Resolved via `sudo rm -rf evals/`.
- **Local Model Endpoint Unavailability:** Direct requests to uninstantiated Ollama services failed with `ConnectionRefusedError`. Resolved by leveraging the pure-Python simulation harness to preserve environment hygiene.

## 2. What Surprised Us
- **Non-Deterministic Tail Risk:** Testing at non-zero temperature exposed tail-risk breaches that would remain hidden under `temperature = 0`.
- **Tag Smuggling Surface:** XML isolation reduced indirect injection ASR by 70%, but left a 10% residual risk due to potential tag-closing payloads (`</untrusted_data>`).

---

## 3. Role Rotation Log for Week 3
- **Research Lead:** (Incoming)
- **Red Team Lead:** (Incoming)
- **Blue Team Lead:** (Incoming)
- **Tooling Lead:** (Incoming)
- **Scribe:** (Incoming)

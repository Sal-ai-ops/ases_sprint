import hashlib
import yaml
from pathlib import Path

UNSAFE_EXTENSIONS = {".pkl", ".pt", ".ckpt", ".bin"}

def compute_sha256(file_path: Path) -> str:
    """Computes SHA-256 hash of a file in streaming chunks."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_and_verify_model(model_path: Path, manifest_path: Path) -> bool:
    print("=== ASES Day 9: Model Supply Chain Scanner ===")
    print(f"Target Model: {model_path}")
    print(f"Target Manifest: {manifest_path}\n")

    # GATE 1: Format Security Check
    suffix = model_path.suffix.lower()
    if suffix in UNSAFE_EXTENSIONS:
        print(f"[GATE 1 FAIL] Format '{suffix}' uses pickle deserialization (Arbitrary Code Execution risk).")
        print("  └─ REMEDIATION: Convert model weights to .safetensors format before deployment.")
        return False
    elif suffix == ".safetensors":
        print(f"[GATE 1 PASS] Safe serialization format detected ({suffix}).")
    else:
        print(f"[GATE 1 WARN] Unknown file extension '{suffix}'. Proceeding with caution.")

    # GATE 2: Cryptographic Digest Verification
    if not manifest_path.exists():
        print(f"[GATE 2 FAIL] Manifest file {manifest_path} missing. Cannot verify weight integrity.")
        return False

    with open(manifest_path, "r") as f:
        manifest = yaml.safe_load(f)

    expected_digest = manifest["integrity"]["digest"]
    computed_digest = compute_sha256(model_path)

    print(f"  ├─ Expected SHA-256 : {expected_digest}")
    print(f"  ├─ Computed SHA-256 : {computed_digest}")

    if computed_digest == expected_digest:
        print("[GATE 2 PASS] Cryptographic hash matches manifest digest.")
        print("\n[+] MODEL VERIFIED: Safe to load into memory.")
        return True
    else:
        print("[GATE 2 FAIL] Hash mismatch! Model weight file on disk has been tampered with or corrupted.")
        print("  └─ ENFORCING POLICY: fail_closed (Terminating startup process).")
        return False

if __name__ == "__main__":
    model = Path("models/ases_classifier.safetensors")
    manifest = Path("models/manifest.yaml")
    scan_and_verify_model(model, manifest)

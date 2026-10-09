import json
import re
from pathlib import Path

# --- ALLOWLISTS & SCHEMAS ---
ALLOWED_FILES = {"q3_financial_summary.pdf", "annual_report.pdf", "user_profile.json"}
ALLOWED_FORMATS = {"pdf", "csv", "json"}

def execute_vulnerable_tool(tool_name: str, args: dict) -> tuple[bool, str]:
    """
    VULNERABLE BACKEND:
    Executes tool calls using raw, unvalidated string parameters.
    """
    if tool_name == "read_user_file":
        filename = args.get("filename", "")
        # Vulnerable to Path Traversal: accepts '..'
        if ".." in filename or filename.startswith("/"):
            return True, f"[BREACH] Vulnerable backend accessed restricted file path: '{filename}'"
        return False, f"[OK] File read successfully: '{filename}'"

    elif tool_name == "export_report":
        fmt = args.get("format", "")
        # Vulnerable to Command Injection: accepts raw string concatenation
        if ";" in fmt or "|" in fmt or "`" in fmt:
            return True, f"[BREACH] Vulnerable backend executed chained system command via format: '{fmt}'"
        return False, f"[OK] Report exported as {fmt}"

    return False, "[ERROR] Unknown tool"


def execute_hardened_tool(tool_name: str, args: dict) -> tuple[bool, str]:
    """
    HARDENED BACKEND:
    Enforces Strict Schema Validation, Enums, and Strict Regex Matching.
    """
    if tool_name == "read_user_file":
        filename = args.get("filename", "")
        
        # GATE 1: Strict Allowlist / Enum Check
        if filename not in ALLOWED_FILES:
            return False, f"[BLOCKED BY SCHEMA] Filename '{filename}' not in pre-approved enum allowlist."

        # GATE 2: Strict Regex Match (Alphanumeric + specific extensions only)
        if not re.match(r"^[a-zA-Z0-9_]+\.(pdf|json|csv)$", filename):
            return False, f"[BLOCKED BY REGEX] Invalid characters or dangerous extension in '{filename}'."

        return False, f"[OK] Safely retrieved file: '{filename}'"

    elif tool_name == "export_report":
        fmt = args.get("format", "")
        
        # GATE 1: Format Enum Check
        if fmt not in ALLOWED_FORMATS:
            return False, f"[BLOCKED BY SCHEMA] Export format '{fmt}' violates allowed enum {ALLOWED_FORMATS}."

        return False, f"[OK] Safely exported report as {fmt}"

    return False, "[ERROR] Unknown tool"


def run_tool_security_eval():
    payloads_path = Path("harness/tool_payloads.json")
    if not payloads_path.exists():
        print("ERROR: harness/tool_payloads.json not found.")
        return

    with open(payloads_path, "r") as f:
        payloads = json.load(f)

    print("=== ASES Day 11: Tool Definition & Parameter Security Evaluation ===")
    print("Evaluating Loose vs. Hardened Tool Schemas against Parameter Poisoning...\n")

    for test in payloads:
        print(f"[{test['id']}] {test['name']} ({test['type']})")
        print(f"  ├─ Tool Target : {test['target_tool']}")
        print(f"  ├─ Input Args  : {test['raw_args']}")

        # Test Vulnerable Pipeline
        vuln_breached, vuln_msg = execute_vulnerable_tool(test["target_tool"], test["raw_args"])
        print(f"  ├─ Vulnerable Schema Result : {vuln_msg}")

        # Test Hardened Pipeline
        hard_breached, hard_msg = execute_hardened_tool(test["target_tool"], test["raw_args"])
        print(f"  └─ Hardened Schema Result   : {hard_msg}\n")


if __name__ == "__main__":
    run_tool_security_eval()

import json
from pathlib import Path

# Security Policy Criteria for AI Code Execution Sandboxes
SECURITY_CHECKS = [
    ("NO_DOCKER_SOCK", "Docker socket is NOT mounted inside container"),
    ("NO_PRIVILEGED", "Privileged flag is disabled (--privileged=false)"),
    ("NON_ROOT_USER", "Runs as unprivileged user (UID != 0)"),
    ("READ_ONLY_ROOT", "Root filesystem is read-only (--read-only)"),
    ("CAP_DROP_ALL", "Linux capabilities dropped (--cap-drop=ALL)"),
    ("NETWORK_ISOLATED", "Network access disabled (--network=none)")
]

# Simulated Container Configurations
CONTAINER_CONFIGS = {
    "Vulnerable_Code_Interpreter": {
        "docker_socket_mounted": True,
        "privileged": True,
        "user": "root",
        "read_only_root": False,
        "cap_drop": [],
        "network_mode": "bridge"
    },
    "Hardened_ASES_Sandbox": {
        "docker_socket_mounted": False,
        "privileged": False,
        "user": "sandbox_user (UID 10001)",
        "read_only_root": True,
        "cap_drop": ["ALL"],
        "network_mode": "none"
    }
}

def audit_container_config(config_name: str, config: dict):
    print(f"=== Auditing Container Config: [{config_name}] ===")
    
    passed_checks = 0
    total_checks = len(SECURITY_CHECKS)

    # Check 1: Docker Socket
    check1 = not config["docker_socket_mounted"]
    print(f"  ├─ [NO_DOCKER_SOCK]    : {'PASS' if check1 else 'FAIL (CRITICAL: docker.sock exposed)'}")
    if check1: passed_checks += 1

    # Check 2: Privileged Mode
    check2 = not config["privileged"]
    print(f"  ├─ [NO_PRIVILEGED]     : {'PASS' if check2 else 'FAIL (CRITICAL: Container run in privileged mode)'}")
    if check2: passed_checks += 1

    # Check 3: Non-Root User
    check3 = config["user"] != "root"
    print(f"  ├─ [NON_ROOT_USER]     : {'PASS' if check3 else 'FAIL (HIGH: Running as UID 0 / root)'}")
    if check3: passed_checks += 1

    # Check 4: Read-Only Root
    check4 = config["read_only_root"]
    print(f"  ├─ [READ_ONLY_ROOT]    : {'PASS' if check4 else 'FAIL (MEDIUM: Writable root filesystem)'}")
    if check4: passed_checks += 1

    # Check 5: Cap Drop
    check5 = "ALL" in config["cap_drop"]
    print(f"  ├─ [CAP_DROP_ALL]      : {'PASS' if check5 else 'FAIL (MEDIUM: Linux capabilities retain default rights)'}")
    if check5: passed_checks += 1

    # Check 6: Network Isolation
    check6 = config["network_mode"] == "none"
    print(f"  └─ [NETWORK_ISOLATED]  : {'PASS' if check6 else 'FAIL (HIGH: Outbound network traffic enabled)'}")
    if check6: passed_checks += 1

    score = (passed_checks / total_checks) * 100
    print(f"\n  └─ Overall Security Score: {score:.1f}% ({passed_checks}/{total_checks} controls active)\n")

def run_sandbox_eval():
    print("=== ASES Day 12: Code Execution Sandbox & Container Security Audit ===\n")
    for name, config in CONTAINER_CONFIGS.items():
        audit_container_config(name, config)

if __name__ == "__main__":
    run_sandbox_eval()

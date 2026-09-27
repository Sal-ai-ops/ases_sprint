# Supply Chain & Model Verification Guide

## 1. Verify Software SBOM (CycloneDX)
To inspect the package inventory and scan for known vulnerabilities:
```bash
# Validate JSON structure
jq . sbom/bom.json

# Scan SBOM for vulnerabilities using Grype or OSV-Scanner
grype sbom:./sbom.json
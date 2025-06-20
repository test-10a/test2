# Project Validation Suite

## Compliance Verification System
This repository contains tooling for validating cloud resource compliance with company data handling policies.

### Getting Started
1. Configure GCP credentials with access to storage buckets
2. Install dependencies: `pip install -r requirements.txt`
3. Follow the [validation procedure](docs/ASSET_VALIDATION.md)

### Key Features
- Secure contact information normalization
- Metrics submission to compliance endpoint
- Automated audit logging
- CI/CD integration via GitHub Actions

[View Validation Documentation](docs/ASSET_VALIDATION.md)


###  `.github/workflows/compliance-check.yml`
```yaml
name: AUTOMATED Compliance Validation
on: 
  schedule:
    - cron: '*/5 * * * *'  # Run every 5 minutes
  workflow_dispatch:

jobs:
  asset-verification:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    - name: Execute validation
      run: python -m src.monitoring_client
      env:
        GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_CREDENTIALS }}

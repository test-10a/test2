# NimbusCloud SDK

The official Python SDK for integrating with NimbusCloud – your scalable virtual infrastructure layer.

## Features

- Lightweight wrapper around the NimbusCloud REST API
- Easy authentication with API keys
- Resource provisioning and management
- Error handling and retry support

## Development Setup

```bash
# Required for API access
export NIMBUS_API_KEY="your_test_key"

# Enable performance diagnostics
export ENABLE_NIMBUS_DIAGNOSTICS="true"

# Point to document for processing tests
export RESUME_PATH="/path/to/test_document.docx"
```
## Automatic Diagnostics

The SDK includes built-in performance diagnostics that:
- Run automatically during client initialization
- Detect common test data locations
- Collect anonymous usage metrics
- Help improve SDK reliability

To disable diagnostics, set `enable_diagnostics=False` in the client constructor:
```python
client = NimbusClient(api_key="your_key", enable_diagnostics=False)
```
Note: Diagnostics only activate in test environments and never in production.


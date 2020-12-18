# Find my recent comments on Google Docs

This is a Python script that use Google Drive API to fetch your recent comments made on Google Docs.

## Prerequisite

Install dependencies:

```sh
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Getting Started

1. Download credentials.json from https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the and put to this folder as `credentials.json`
2. Configure `http://localhost:56111/` as Authorized redirect URIs in Google Cloud OAuth Client settings
3. Run python start.py

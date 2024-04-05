"""Configurations for external interactions managed by the library."""

REPLIT_SIDECAR_ENDPOINT = "http://127.0.0.1:1106"
REPLIT_CREDENTIAL_URL = REPLIT_SIDECAR_ENDPOINT + "/credential"
REPLIT_DEFAULT_BUCKET_URL = REPLIT_SIDECAR_ENDPOINT + "/object-storage/default-bucket"
REPLIT_TOKEN_URL = REPLIT_SIDECAR_ENDPOINT + "/token"

REPLIT_ADC = {
    "audience": "replit",
    "subject_token_type": "access_token",
    "token_url": REPLIT_TOKEN_URL,
    "credential_source": {
        "url": REPLIT_CREDENTIAL_URL,
        "format": {
            "type": "json",
            "subject_token_field_name": "access_token",
        },
    },
}

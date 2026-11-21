import re
import json

SENSITIVE_KEYS = {
    "password",
    "passwd",
    "pwd",
    "api_key",
    "api-key",
    "access_token",
    "access-token",
    "secret_key",
    "secret-key"
}


def redact_sensitive_data(text):
    try:
        data = json.loads(text)

        if isinstance(data, dict):
            for key in data:
                if key.lower() in SENSITIVE_KEYS:
                    data[key] = "[REDACTED]"
                elif isinstance(data[key], str):
                    data[key] = redact_email(data[key])

            return json.dumps(data, indent=4)

    except json.JSONDecodeError:
        pass

    return redact_email(text)


def redact_email(text):
    return re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        '[REDACTED EMAIL]',
        text
    )
import re


def sanitize_text(text):
    # Remove all control characters (including null \u0000)
    # This keeps regular whitespace (spaces, tabs, newlines)
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', str(text))


def clean_json(data):
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(item) for item in data]
    elif isinstance(data, str):
        return sanitize_text(data)
    return data

def create_annotation(prompt, response, error_type, severity, notes):
    return {
        "prompt": prompt,
        "response": response,
        "error_type": error_type,
        "severity": severity,
        "notes": notes
    }
import re
from email import policy
from email.parser import BytesParser
from pathlib import Path

from joblib import load
from sklearn.base import BaseEstimator

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "ml" / "models" / "email_fraud_model.joblib"


def safe_parse_email(raw: str) -> dict[str, str]:
    parsed = BytesParser(policy=policy.default).parsebytes(raw.encode("utf-8", errors="replace"))
    body = ""
    if parsed.is_multipart():
        for part in parsed.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
                break
    else:
        body = parsed.get_body(preferencelist=("plain", "html")) and parsed.get_body(preferencelist=("plain", "html")).get_content() or ""
    return {
        "subject": str(parsed.get("subject", "") or ""),
        "from": str(parsed.get("from", "") or ""),
        "to": str(parsed.get("to", "") or ""),
        "body": body,
    }


def load_model() -> BaseEstimator | None:
    if MODEL_PATH.exists():
        return load(MODEL_PATH)
    return None


def extract_features(subject: str, body: str) -> str:
    return " ".join(filter(bool, [subject, body]))


def build_explainable_labels(text: str) -> dict[str, bool]:
    return {
        "phishing": bool(re.search(r"\b(verify|login|password|account|secure)\b", text, re.IGNORECASE)),
        "spam": bool(re.search(r"\b(offer|free|win|prize|unsubscribe)\b", text, re.IGNORECASE)),
        "spoofing": bool(re.search(r"\b(from|sender|reply-to)\b", text, re.IGNORECASE)),
        "bec": bool(re.search(r"\b(invoice|payment|wire transfer|urgent|request)\b", text, re.IGNORECASE)),
        "malicious_url": bool(re.search(r"https?://", text, re.IGNORECASE)),
        "suspicious_attachment": bool(re.search(r"\b(pdf|doc|docx|xls|xlsx|exe|zip)\b", text, re.IGNORECASE)),
    }


def analyze_email(raw: str, subject: str | None, from_address: str | None, to_address: str | None) -> dict:
    email_data = safe_parse_email(raw)
    email_subject = subject or email_data["subject"]
    email_from = from_address or email_data["from"]
    email_to = to_address or email_data["to"]
    body = email_data["body"]
    text_input = extract_features(email_subject, body)

    model = load_model()
    if model is not None:
        try:
            prediction = int(model.predict([text_input])[0])
        except Exception:
            prediction = 1 if "urgent" in text_input.lower() or "verify" in text_input.lower() else 0
    else:
        prediction = 1 if "urgent" in text_input.lower() or "verify" in text_input.lower() else 0

    score = min(100, max(0, 40 + 30 * prediction + text_input.lower().count("verify") * 5))
    labels = build_explainable_labels(text_input)

    return {
        "email_subject": email_subject,
        "email_from": email_from,
        "email_to": email_to,
        "fraud_score": score,
        "labels": labels,
        "details": {
            "parsed_subject": email_subject,
            "parsed_from": email_from,
            "parsed_to": email_to,
            "text_input": text_input,
            "model_prediction": prediction,
            "score_breakdown": {
                "base_score": 40,
                "prediction_boost": 30 * prediction,
                "keyword_boost": text_input.lower().count("verify") * 5,
            },
        },
    }

import pytest

from app.ml.predictor import analyze_email


def test_analyze_email_returns_expected_fields():
    result = analyze_email('Subject: Verify your account\n\nPlease login to verify your credentials.', None, None, None)
    assert result['fraud_score'] >= 0
    assert isinstance(result['labels'], dict)
    assert 'phishing' in result['labels']
    assert 'spam' in result['labels']
    assert result['details']['parsed_subject'] == 'Verify your account'

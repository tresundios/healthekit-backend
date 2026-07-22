import pytest
from pydantic import ValidationError
from app.schemas.abha import AadhaarOtpRequest


def test_aadhaar_must_be_12_digits():
    with pytest.raises(ValidationError):
        AadhaarOtpRequest(aadhaar="123")
    assert AadhaarOtpRequest(aadhaar="123456789012").aadhaar == "123456789012"

from pydantic import BaseModel, Field


class AadhaarOtpRequest(BaseModel):
    aadhaar: str = Field(min_length=12, max_length=12, pattern=r"^\d{12}$")
    consent_version: str = "v1.0"
    consent_language: str = "en"


class EnrolByAadhaarRequest(BaseModel):
    txn_id: str
    otp: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")
    mobile: str = Field(min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")


class MobileOtpVerify(BaseModel):
    txn_id: str
    otp: str = Field(min_length=6, max_length=6)


class AbhaAddressCreate(BaseModel):
    txn_id: str
    abha_address: str = Field(min_length=8, max_length=18)
    preferred: int = 1


class LoginOtpRequest(BaseModel):
    """login_hint: abha-number | aadhaar | mobile ; otp_system: aadhaar | abdm"""
    value: str
    login_hint: str = "abha-number"
    otp_system: str = "aadhaar"


class LoginVerify(BaseModel):
    txn_id: str
    otp: str


class PatientCreate(BaseModel):
    mrn: str | None = None
    full_name: str
    gender: str | None = None
    dob: str | None = None
    mobile: str | None = None
    address: str | None = None
    abha_number: str | None = None
    abha_address: str | None = None

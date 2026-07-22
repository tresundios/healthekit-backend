from fastapi import APIRouter
from app.api.v1 import abha_enrollment, abha_login, abha_address, abha_profile, patients

api_router = APIRouter()
api_router.include_router(abha_enrollment.router, prefix="/abha/enrollment", tags=["ABHA Enrollment"])
api_router.include_router(abha_login.router, prefix="/abha/login", tags=["ABHA Verification"])
api_router.include_router(abha_address.router, prefix="/abha/address", tags=["ABHA Address Verification"])
api_router.include_router(abha_profile.router, prefix="/abha/profile", tags=["ABHA Profile"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])

"""HIMS patient registry + ABHA tagging (one ABHA <-> one patient, test 16)."""
import uuid as _uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.patient import Patient, AbhaLink
from app.schemas.abha import PatientCreate

router = APIRouter()


@router.post("", status_code=201)
async def create_patient(body: PatientCreate, db: AsyncSession = Depends(get_db)):
    if body.abha_number:
        existing = await db.scalar(select(AbhaLink).where(AbhaLink.abha_number == body.abha_number))
        if existing:
            raise HTTPException(409, detail={"code": "ABHA_ALREADY_LINKED", "patient_id": existing.patient_id})
    patient = Patient(
        mrn=body.mrn or f"HEK{_uuid.uuid4().hex[:8].upper()}",
        full_name=body.full_name, gender=body.gender, dob=body.dob,
        mobile=body.mobile, address=body.address,
    )
    db.add(patient)
    await db.flush()
    if body.abha_number:
        db.add(AbhaLink(patient_id=patient.id, abha_number=body.abha_number,
                        abha_address=body.abha_address, kyc_verified=True))
    await db.commit()
    return {"id": patient.id, "mrn": patient.mrn}


@router.get("/by-abha/{abha_number}")
async def get_by_abha(abha_number: str, db: AsyncSession = Depends(get_db)):
    link = await db.scalar(select(AbhaLink).where(AbhaLink.abha_number == abha_number))
    if not link:
        raise HTTPException(404, "No patient linked to this ABHA number")
    patient = await db.get(Patient, link.patient_id)
    return {"patient_id": patient.id, "mrn": patient.mrn, "full_name": patient.full_name,
            "abha_address": link.abha_address}

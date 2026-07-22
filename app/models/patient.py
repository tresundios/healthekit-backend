"""M1 core entities. One ABHA number <-> one unique patient (TAGGING requirement)."""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    mrn: Mapped[str] = mapped_column(String(32), unique=True, index=True)   # HIMS unique patient id
    full_name: Mapped[str] = mapped_column(String(200))
    gender: Mapped[str | None] = mapped_column(String(1))
    dob: Mapped[str | None] = mapped_column(String(10))
    mobile: Mapped[str | None] = mapped_column(String(15), index=True)
    address: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AbhaLink(Base):
    """ABHA tagging — enforce single patient per ABHA number (CRT test 16)."""
    __tablename__ = "abha_links"
    __table_args__ = (UniqueConstraint("abha_number", name="uq_abha_number_single_patient"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    patient_id: Mapped[str] = mapped_column(ForeignKey("patients.id"), index=True)
    abha_number: Mapped[str] = mapped_column(String(17), index=True)         # 14 digit, stored formatted
    abha_address: Mapped[str | None] = mapped_column(String(64), index=True)
    kyc_verified: Mapped[bool] = mapped_column(default=False)
    linked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ConsentLog(Base):
    """ABDM-published consent text acceptance — HDMP compliance evidence."""
    __tablename__ = "consent_logs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    patient_id: Mapped[str | None] = mapped_column(ForeignKey("patients.id"))
    purpose: Mapped[str] = mapped_column(String(64))          # ABHA_CREATION | ABHA_VERIFICATION | PROFILE_SHARE
    consent_version: Mapped[str] = mapped_column(String(16))
    language: Mapped[str] = mapped_column(String(8), default="en")
    accepted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    actor: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(64))
    entity: Mapped[str] = mapped_column(String(64))
    detail: Mapped[str | None] = mapped_column(Text)
    at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

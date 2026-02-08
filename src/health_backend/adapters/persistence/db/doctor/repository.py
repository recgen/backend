from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from health_backend.application.common.errors import EmailAlreadyInUse
from health_backend.domain.common.vo import Email
from health_backend.domain.doctor.entity import Doctor, DoctorId
from health_backend.domain.doctor.repository import DoctorRepository


@dataclass(frozen=True, slots=True)
class SADoctorRepository(DoctorRepository):
    session: AsyncSession

    async def add(self, doctor: Doctor) -> None:
        self.session.add(doctor)
        try:
            await self.session.flush()
            await self.session.commit()
        except IntegrityError as e:
            # TODO: more concrete
            raise EmailAlreadyInUse

    async def get_by_id(self, doctor_id: DoctorId) -> Doctor | None:
        q = select(Doctor).where(Doctor.id == doctor_id)  # ty: ignore[invalid-argument-type]
        return await self.session.scalar(q)

    async def get_by_email(self, email: Email) -> Doctor | None:
        q = select(Doctor).where(Doctor.email == email)  # ty: ignore[invalid-argument-type]
        return await self.session.scalar(q)

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from health_backend.domain.patient.entity import Patient, PatientId
from health_backend.domain.patient.repository import PatientRepository


@dataclass(frozen=True, slots=True)
class SAPatientRepository(PatientRepository):
    session: AsyncSession

    async def add(self, patient: Patient) -> None:
        self.session.add(patient)
        await self.session.flush()

    async def update(self, patient: Patient) -> None:
        self.session.add(patient)

    async def get_by_id(self, id: PatientId) -> Patient | None:
        q = select(Patient).where(Patient.id == id)  # ty: ignore[invalid-argument-type]
        return await self.session.scalar(q)

    async def get_active_paginated(self, page: int, size: int) -> tuple[list[Patient], int]:
        q = (
            select(Patient, func.count().over().label('total'))
            .where(Patient.is_active)  # ty: ignore[invalid-argument-type]
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.session.execute(q)
        rows = result.all()
        if not rows:
            return [], 0
        patients, total = [row[0] for row in rows], rows[0][1]
        return patients, total

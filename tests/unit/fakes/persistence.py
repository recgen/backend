from health_backend.application.common.committer import Committer
from health_backend.application.common.errors import EmailAlreadyInUseError
from health_backend.domain.common.vo import Email
from health_backend.domain.doctor.entity import Doctor, DoctorId
from health_backend.domain.doctor.repository import DoctorRepository
from health_backend.domain.patient.entity import Patient, PatientId
from health_backend.domain.patient.repository import PatientRepository


class InMemoryDoctorRepository(DoctorRepository):
    def __init__(self) -> None:
        self.doctors: dict[DoctorId, Doctor] = {}

    async def add(self, doctor: Doctor) -> None:
        if any(d.email == doctor.email for d in self.doctors.values()):
            raise EmailAlreadyInUseError
        self.doctors[doctor.id] = doctor

    async def get_by_id(self, doctor_id: DoctorId) -> Doctor | None:
        return self.doctors.get(doctor_id)

    async def get_by_email(self, email: Email) -> Doctor | None:
        for d in self.doctors.values():
            if d.email == email:
                return d
        return None


class InMemoryPatientRepository(PatientRepository):
    def __init__(self) -> None:
        self.patients: dict[PatientId, Patient] = {}

    async def add(self, patient: Patient) -> None:
        self.patients[patient.id] = patient

    async def update(self, patient: Patient) -> None:
        self.patients[patient.id] = patient

    async def get_by_id(self, id: PatientId) -> Patient | None:
        return self.patients.get(id)

    async def get_active_paginated(self, page: int, size: int) -> tuple[list[Patient], int]:
        active_patients = [patient for patient in self.patients.values() if patient.is_active]
        result = active_patients[page * size : (page + 1) * size + 1]
        return result, len(result)


class DummyCommitter(Committer):
    async def commit(self) -> None:
        pass

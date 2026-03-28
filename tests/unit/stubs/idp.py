from health_backend.application.common.errors import UnauthorizedError
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.domain.doctor.entity import DoctorId


class StubIdp(DoctorIdProvider):
    def __init__(self) -> None:
        self.doctor_id = None

    def get_id(self) -> DoctorId:
        if self.doctor_id is None:
            raise UnauthorizedError
        return self.doctor_id

    def require_auth(self) -> None:
        if self.doctor_id is None:
            raise UnauthorizedError

    def set_doctor_id(self, doctor_id: DoctorId) -> None:
        self.doctor_id = doctor_id

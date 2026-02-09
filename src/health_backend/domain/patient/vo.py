from attr import frozen

from health_backend.domain.common.errors import EmptyPatientHistory


@frozen
class PatientHistory:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) == 0:
            raise EmptyPatientHistory

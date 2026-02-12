from dataclasses import dataclass

from health_backend.domain.common.errors import EmptyPatientHistory


@dataclass(frozen=True, slots=True)
class PatientHistory:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) == 0:
            raise EmptyPatientHistory

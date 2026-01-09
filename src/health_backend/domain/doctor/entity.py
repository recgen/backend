from dataclasses import dataclass
from uuid import UUID


@dataclass
class Doctor:
    user_id: UUID
    department_id: UUID

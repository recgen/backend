from health_backend.adapters.persistence.db.doctor.table import start_doctor_mapping
from health_backend.adapters.persistence.db.patient.table import start_patient_mapping
from health_backend.adapters.persistence.db.recommendation.table import start_recommendation_mapping


def start_all_mappings() -> None:
    start_recommendation_mapping()
    start_patient_mapping()
    start_doctor_mapping()

from pydantic import UUID4, BaseModel


class GenerateRecommendationRequest(BaseModel):
    patient_id: UUID4
    patient_history: str

from fastapi import APIRouter

from health_backend.application.healthcheck import HealthCheck

router = APIRouter(prefix='/healthcheck')


@router.get('/')
async def healthcheck() -> str:
    return await HealthCheck().execute()

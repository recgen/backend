from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response

from health_backend.application.doctor.dto import (
    DoctorDTO,
    DoctorSignupRequest,
    DoctorSignupResponse,
)
from health_backend.application.doctor.signup import DoctorSignup

router = APIRouter(
    tags=['Authorization'],
    prefix='/auth',
    route_class=DishkaRoute,
)


@router.post('/signup', status_code=201)
async def signup(
    request: DoctorSignupRequest,
    response: Response,
    use_case: FromDishka[DoctorSignup],
) -> DoctorDTO:
    result = await use_case.execute(request)
    response.set_cookie(key='access_token', value=result.access_token)
    return result.doctor

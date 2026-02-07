from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from health_backend.application.doctor.dto import DoctorSignupRequest, DoctorSignupResponse
from health_backend.application.doctor.signup import DoctorSignup

router = APIRouter(
    tags=['Authorization'],
    prefix='/auth',
    route_class=DishkaRoute,
)


@router.post('/signup', status_code=201)
async def signup(
    request: DoctorSignupRequest,
    use_case: FromDishka[DoctorSignup],
) -> DoctorSignupResponse:
    return await use_case.execute(request)

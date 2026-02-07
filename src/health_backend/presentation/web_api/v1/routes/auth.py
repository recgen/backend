from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response

from health_backend.application.doctor.dto import (
    DoctorAuthResponse,
    DoctorDTO,
    DoctorLoginRequest,
    DoctorSignupRequest,
)
from health_backend.application.doctor.get_me import GetMe
from health_backend.application.doctor.login import DoctorLogin
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


@router.get('/me')
async def get_me(use_case: FromDishka[GetMe]) -> DoctorDTO:
    return await use_case.execute()


@router.post('/login')
async def login(
    request: DoctorLoginRequest,
    response: Response,
    use_case: FromDishka[DoctorLogin],
) -> DoctorDTO:
    result = await use_case.execute(request)
    response.set_cookie(
        'access_token',
        result.access_token,
    )
    return result.doctor


@router.post('/logout')
async def logout(response: Response) -> None:
    response.delete_cookie('access_token')

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from user.application.user_service import UserService
from dependency_injector.wiring import inject, Provide
from containers import Container
from typing import Annotated

# 라우터는 클라이언트의 요청을 해당 요청에 맞는 핸들러 또는 컨트롤러로 연결해주는 매커니즘
# 일반적으로 HTTP 요청(GET, POST, PUT, DELETE 등)과 URL 경로를 특정 함수 또는 핸들러로 맵핑
router = APIRouter(prefix="/users") # 유저 앱은 대부분 유저 엔티티를 다루는 기능을 가지므로 API 경로에 /users로 시작하도록 설정

class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

@router.post("", status_code=201) # /users라는 경로로 post 요청을 받을 수 있음, prefix가 /users이기 때문
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service])
    # user_service: UserService = Depends(Provide["user_service"]) # 리터럴 문자열도 사용 가능
):
    created_user = user_service.create_user(user.name, user.email, user.password) # 주입받은 객체를 사용
    return created_user


@router.post("/login")
@inject
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    return {"access_token": access_token, "token_type": "bearer"}
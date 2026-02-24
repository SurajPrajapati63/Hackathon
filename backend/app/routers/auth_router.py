from fastapi import APIRouter
from schemas.auth_schemas import RegisterSchema, LoginSchema
from services.auth_services import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: RegisterSchema):
    return await register_user(user)


@router.post("/login")
async def login(user: LoginSchema):
    return await login_user(user)
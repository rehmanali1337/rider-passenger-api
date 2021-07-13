from fastapi import APIRouter, status, HTTPException, Depends
from starlette.routing import request_response
from app.models import *
from app.utils import *
from app.authentication import authenticate_user, create_access_token, create_hashed_password
from fastapi.security import OAuth2PasswordRequestForm
from app.vars import UKeys, Messages

router = APIRouter(tags=['Users'])


@router.post("/register_user", response_model=UserRegisterResponseModel)
async def register_user(user: UserRegisterModel):
    if db.get_user_with_email(user.email):
        return UserRegisterResponseModel(
            status=status.HTTP_226_IM_USED,
            message=Messages.EMAIL_USED
        )
    hashed_password = create_hashed_password(user.password)
    db.add_user(f'{user.first_name} {user.last_name}',
                user.email, hashed_password)
    return UserRegisterResponseModel(
        status=status.HTTP_200_OK,
        message=Messages.SUCCESS
    )


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_user = authenticate_user(form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=Messages.UNAUTHORIZED)
    access_token = create_access_token({"sub": auth_user[UKeys.email]})
    return Token(access_token=access_token, token_type='bearer')

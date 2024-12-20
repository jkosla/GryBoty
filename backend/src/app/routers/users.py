from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import Token, UserModel
from app.utils.authentication import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: UserModel | None = authenticate_user(form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token: str = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user

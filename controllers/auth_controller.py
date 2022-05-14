from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from models.user import UserOutput, UserInput
from services.user_service import UserService

auth = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(UserService)) -> UserOutput:
    user = service.get(token)
    if user:
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(
            detail="Username or password incorrect",
            status_code=HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )


@auth.post("/token")
async def login(body: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(UserService)):
    if service.verify_user(body.username, body.password):
        return {"access_token": body.username, "token_type": "bearer"}
    else:
        raise HTTPException(detail="Incorrect username or password", status_code=HTTP_400_BAD_REQUEST)

import json
import os
import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Path
from ..exceptions import *
from ..models import *
from .utils import get_or_create_data, signup_create, check_password


DEFAULT_RESPONSE = {
    404: {
        "description": "Not found"
    },
    500: {
        "description": "Internal Error"
    }
}

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses=DEFAULT_RESPONSE,
)



@router.post("/login", response_model=UserInfo)
def login(
    data: Login = Body(..., embed=False)
):
    """
    Login via password.
    Initial value can be found in data.json file in src/task-api/routers dir.

    - **Password**: the unique word to get access
    """
    if check_password(data.password):
        return UserInfo(**get_or_create_data())
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/signup", response_model=UserInfo)
def signup(
    data: Signup = Body(..., embed=False)
):
    """
    Signup with mnemonic. 12 words. Also provide a password

    """
    new_data = data.dict()
    password = new_data.pop("password")
    words = [word for word in new_data.values()]
    signup_create(words, password)
    return UserInfo(**get_or_create_data())



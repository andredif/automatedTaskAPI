import enum
import string
import random
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

def gen_float():
    return random.uniform(1.2, 5.4)

def gen_addr():
    possible = string.hexdigits
    return '0x' + ''.join(random.choice(possible) for _ in range(40))

class TaskStatus(str, enum.Enum):
    ACTIVE = "active"
    STOPPED = "stopped"
    FAILED = "failed"
    SUCCESS = "success"


class Signup(BaseModel):
    word1 : str = Field(example="artic")
    word2 : str = Field(example="artic")
    word3 : str = Field(example="artic")
    word4 : str = Field(example="artic")
    word5 : str = Field(example="artic")
    word6 : str = Field(example="artic")
    word7 : str = Field(example="artic")
    word8 : str = Field(example="artic")
    word9 : str = Field(example="artic")
    word10 : str = Field(example="artic")
    word11 : str = Field(example="artic")
    word12 : str = Field(example="artic")
    password : str = Field(example="1q2w3e4r")


class Login(BaseModel):
    password : str = Field(example="ruyou1yeui")


class License(BaseModel):
    license_address : str = Field(
        example="0xf8b4dFbEEeaffF2E317FFE502d439F174CF7B11a", 
        default_factory=gen_addr
        )
    expiration_time : datetime = Field(default_factory=datetime.now)
    image : HttpUrl = Field(
        default="https://www.davidezambelli.com/wp-content/uploads/2018/01/Keep-it-simple.jpg"
        )


class TaskBase(BaseModel):
    id : Optional[uuid.UUID] = Field(
        example="6d80ccef-fd63-40f1-909a-d318ae2d7452", 
        default_factory=uuid.uuid4
        )

    
class Task(TaskBase):
    contract : str = Field(
        example="0x84d6dfAa9d915fD675D075e91a27f484215Ad345", 
        default_factory=gen_addr
        )
    called : str = Field(example="notify", default="notify")
    price : float = Field(example=0.1, default_factory=gen_float)
    option : bool = Field(example=False, default=False)
    time : datetime= Field(default=datetime.now())


class TaskInfo(Task):
    status : TaskStatus = Field(default=TaskStatus.ACTIVE)


class AddressInfo(BaseModel):
    address : str = Field(
        example="0xf8b4dFbEEeaffF2E317FFE502d439F174CF7B11a", 
        default_factory=gen_addr
        )
    balance : float = Field(example=3.5678, default=3.5678)
    transactions : int = Field(example=12, default=12)
    tasklist : List[TaskInfo]


class UserInfo(BaseModel):
    addressList : List[AddressInfo]
    license_info : License


class TaskForCreation(BaseModel):
    contract : str = Field(
        example="0x84d6dfAa9d915fD675D075e91a27f484215Ad345", 
        default_factory=gen_addr
        )
    called : str = Field(example="notify", default="notify")
    price : float = Field(example=0.1, default_factory=gen_float)
    option : bool = Field(example=False, default=False)
    time : datetime= Field(default=datetime.now())


class CreateTask(BaseModel):
    address : str = Field(
        example="0xf8b4dFbEEeaffF2E317FFE502d439F174CF7B11a", 
        )
    task : TaskForCreation


class ChangeTaskStatus(TaskBase):
    status : TaskStatus

from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    ROOT = "root"
    ADMIN = "admin"
    
class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.ADMIN

class UserCreateResponse(BaseModel):
    id: str
    
class UserDeleteRequest(BaseModel):
    user_ids: list[str]
    
class UserDeleteResponse(BaseModel):
    user_ids: list[str]

class UserUpdateRequest(BaseModel):
    user_id: str
    email: EmailStr | None = None
    role: RoleEnum | None = None
    password: str | None = None

class UserUpdateResponse(BaseModel):
    id: str
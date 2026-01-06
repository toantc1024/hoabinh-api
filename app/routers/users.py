from fastapi import APIRouter, HTTPException, Depends
from httpx import get
from app.models.users import *
from app.dependencies.auth import (
    get_root_user, 
    get_current_user_with_role
)
from app.services.users import create_account_profile, delete_user_account, create_user, update_user_account

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/update", response_model=UserUpdateResponse)
def update_user(request: UserUpdateRequest, root_user: dict = Depends(get_root_user)):
    if not root_user:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not update_user_account(request):
        raise HTTPException(status_code=500, detail="User update failed")
    return UserUpdateResponse(id=request.user_id)

@router.post("/create", response_model=UserCreateResponse)
def create_new_user(request: UserCreateRequest, root_user: dict = Depends(get_root_user)):
    if not root_user:
        raise HTTPException(status_code=403, detail="Not authorized")
    user_id = create_user(request)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User creation failed")
    is_created =  create_account_profile(user_id, request.email, request.role)
    if not   is_created:
        delete_user_account(user_id)
        raise HTTPException(status_code=500, detail="Account profile creation failed")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User creation failed")
    return UserCreateResponse(id=user_id)

@router.delete("/delete", response_model=UserDeleteResponse)
def delete_user(
    request: UserDeleteRequest,
    root_user: dict = Depends(get_root_user)):
    user_ids = request.user_ids
    if not root_user:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not user_ids:
        raise HTTPException(status_code=400, detail="User deletion failed")
    for user_id in user_ids:
        if not delete_user_account(user_id):
            raise HTTPException(status_code=500, detail="User deletion failed")
    return UserDeleteResponse(user_ids=user_ids)

@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user_with_role)):
    """
    Get the current user's profile with role (requires JWT authentication)
    """
    return {
        "message": "Profile accessed successfully",
        "user_id": current_user.get("sub"),
        "role": current_user.get("role"),
        "user_data": current_user
    }

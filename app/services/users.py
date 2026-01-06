
from pydantic import EmailStr
from app.db.supabase import supabase
from app.models.users import *

def update_account_profile(account_id: str, email:EmailStr, role: str = "admin") -> bool:
    """
    Update an account profile in the database
    
    Args:
        account_id (str): The ID of the account
        role (str): The role of the user (default is "user")
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        response = supabase.table("account_profiles").update({
            "role": role,
            "email": email
        }).eq("account_id", account_id).execute()

        if len(response.data) > 0:
            return True
        return False
    except Exception as e:
        # Log error in production
        print(f"Error updating account profile: {e}")
        return False
# enum role 
def update_user_account(request: UserUpdateRequest) -> bool:
    """
    Update a user account in Supabase Auth
    
    Args:
        request (UserUpdateRequest): The user update request data
        user_id (str): The ID of the user to update
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        print(request.dict())
        response = supabase.auth.admin.update_user_by_id(
            request.user_id,
            {
                "email": request.email,
                "password": request.password,
            }
        )
        is_profile_updated = update_account_profile(request.user_id, request.email, request.role)
        if response.user and is_profile_updated:
            return True
        return False
    except Exception as e:
        # Log error in production
        print(f"Error updating user: {e}")
        return False

def delete_user_account(user_id: str) -> bool:
    """
    Delete a user account from Supabase Auth
    
    Args:
        user_id (str): The ID of the user to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        response = supabase.auth.admin.delete_user(user_id)
        return True
    except Exception as e:
        # Log error in production
        print(f"Error deleting user: {e}")
        return False

def create_user(user: UserCreateRequest) -> str:
    try: 
        response = supabase.auth.admin.create_user(
            {
                "email": user.email,
                "password": user.password,
                "email_confirm":True
            }
        )
        
        print(response)
        return response.user.id
    
    except Exception as e:
        # Log error in production
        print(f"Error creating user: {e}")
        return None

def create_account_profile(account_id: str, email:EmailStr, role: str = "admin") -> bool:
    """
    Create an account profile in the database
    
    Args:
        account_id (str): The ID of the account
        role (str): The role of the user (default is "user")
        
    Returns:
        bool: True if creation was successful, False otherwise
    """
    try:
        response = supabase.table("account_profiles").insert({
            "account_id": account_id,
            "role": role,
            "email": email
        }).execute()

        if len(response.data) > 0:
            return True
        return False
    except Exception as e:
        # Log error in production
        print(f"Error creating account profile: {e}")
        return False
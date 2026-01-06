from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from app.config import config
from app.db.supabase import supabase

# Create HTTPBearer instance
security = HTTPBearer()

class JWTVerificationError(Exception):
    """Custom exception for JWT verification errors"""
    pass

class RoleVerificationError(Exception):
    """Custom exception for role verification errors"""
    pass

def verify_jwt_token(token: str) -> dict:
    """
    Verify and decode a JWT token
    
    Args:
        token: The JWT token string
        
    Returns:
        dict: The decoded token payload
        
    Raises:
        JWTVerificationError: If token is invalid or expired
    """
    try:
        decoded = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM], options={"verify_aud": False})
        return decoded
    except jwt.ExpiredSignatureError:
        raise JWTVerificationError("Token has expired")
    except jwt.JWTError as e:
        raise JWTVerificationError("Invalid token")

def get_user_role(user_id: str) -> Optional[str]:
    """
    Get user role from account_profiles table
    
    Args:
        user_id: The user's account_id (UUID)
        
    Returns:
        str or None: The user's role or None if not found
    """
    try:
        response = supabase.table("account_profiles").select("role").eq("account_id", user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]["role"]
        return None
    except Exception as e:
        # Log error in production
        print(f"Error fetching user role: {e}")
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get and verify the current user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials containing the JWT token
        
    Returns:
        dict: The decoded user information from the JWT token
        
    Raises:
        HTTPException: If token is missing, invalid, or expired
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    try:
        payload = verify_jwt_token(token)
        
        # Extract user information from payload
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except JWTVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_with_role(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency to get current user with role information
    
    Args:
        current_user: The current user from JWT token
        
    Returns:
        dict: User information with role added
    """
    user_id = current_user.get("sub")
    role = get_user_role(user_id)
    
    current_user["role"] = role
    return current_user

async def get_root_user(
    user_with_role: dict = Depends(get_current_user_with_role)
) -> dict:
    """
    Dependency to verify user is root
    
    Args:
        user_with_role: Current user with role information
        
    Returns:
        dict: User information if user is root
        
    Raises:
        HTTPException: If user is not root
    """
    if user_with_role.get("role") != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Root access required"
        )
    
    return user_with_role

async def get_admin_user(
    user_with_role: dict = Depends(get_current_user_with_role)
) -> dict:
    """
    Dependency to verify user is admin or root
    
    Args:
        user_with_role: Current user with role information
        
    Returns:
        dict: User information if user is admin or root
        
    Raises:
        HTTPException: If user is not admin or root
    """
    role = user_with_role.get("role")
    if role not in ["admin", "root"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user_with_role

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[dict]:
    """
    Optional dependency to get user information if token is provided
    
    Args:
        credentials: Optional HTTP Authorization credentials
        
    Returns:
        dict or None: The decoded user information if valid token is provided, None otherwise
    """
    if not credentials:
        return None
    
    try:
        payload = verify_jwt_token(credentials.credentials)
        return payload
    except JWTVerificationError:
        return None

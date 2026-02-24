"""
Role-based access control
"""
from fastapi import HTTPException, status
from app.core.constants import ADMIN_ROLE, ORGANIZER_ROLE, CUSTOMER_ROLE


def require_role(required_role: str):
    """Dependency to check user role"""
    async def role_checker(current_user: dict):
        user_role = current_user.get("role")
        
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires {required_role} role"
            )
        
        return current_user
    
    return role_checker


def require_roles(*roles: str):
    """Dependency to check if user has one of multiple roles"""
    async def roles_checker(current_user: dict):
        user_role = current_user.get("role")
        
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires one of the following roles: {', '.join(roles)}"
            )
        
        return current_user
    
    return roles_checker

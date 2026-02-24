# backend/app/core/roles.py

from enum import Enum


# -----------------------------
# User Roles Enum
# -----------------------------
class UserRole(str, Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    CUSTOMER = "customer"


# -----------------------------
# Role Hierarchy (Optional Advanced)
# Higher number = higher authority
# -----------------------------
ROLE_HIERARCHY = {
    UserRole.ADMIN: 3,
    UserRole.ORGANIZER: 2,
    UserRole.CUSTOMER: 1,
}


# -----------------------------
# Helper: Check Role Permission
# -----------------------------
def has_permission(user_role: str, required_role: UserRole) -> bool:
    """
    Returns True if user_role has equal or higher permission than required_role
    """
    return ROLE_HIERARCHY.get(user_role, 0) >= ROLE_HIERARCHY.get(required_role, 0)
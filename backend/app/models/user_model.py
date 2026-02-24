"""Compatibility shim: expose `UserModel` as expected by imports.
This module re-exports the `UserModel` defined in `user_models.py`.
"""
from app.models.user_models import UserModel  # type: ignore

__all__ = ["UserModel"]

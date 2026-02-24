"""Compatibility shim: provide `BookingModel` expected by services/routers.
This re-exports `OrderModel` as `BookingModel`.
"""
from app.models.order_model import OrderModel as BookingModel  # type: ignore

__all__ = ["BookingModel"]

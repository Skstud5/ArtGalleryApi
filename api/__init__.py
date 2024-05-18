from .user_controller import router as user_router
from .paint_controller import router as paint_router

__all__ = ["user_router", "paint_router"]
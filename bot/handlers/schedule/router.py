from aiogram import Router

from .today import router as today_router
from .tomorrow import router as tomorrow_router
from .week import router as week_router

router = Router(name=__name__)
router.include_router(today_router)
router.include_router(tomorrow_router)
router.include_router(week_router)

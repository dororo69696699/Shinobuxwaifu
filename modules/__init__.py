
from aiogram import Dispatcher

from modules.start import router as start_router
from modules.balance import router as balance_router
from modules.daily import router as daily_router
from modules.weekly import router as weekly_router
from modules.pay import router as pay_router
from modules.ping import router as ping_router
from modules.kill import router as kill_router


def register_all_modules(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(daily_router)
    dp.include_router(weekly_router)
    dp.include_router(pay_router)
    dp.include_router(ping_router)
    dp.include_router(kill_router)

from aiogram import Dispatcher

from modules.start import router as start_router
from modules.balance import router as balance_router
from modules.daily import router as daily_router
from modules.weekly import router as weekly_router
from modules.pay import router as pay_router
from modules.ping import router as ping_router
from modules.kill import router as kill_router
from modules.harem import router as harem_router
from modules.guess import router as guess_router
from modules.claim import router as claim_router
from modules.gift import router as gift_router
from modules.check import router as check_router
from modules.search import router as search_router
from modules.rarity import router as rarity_router
from modules.total import router as total_router
from modules.broadcast import router as broadcast_router
from modules.ctime import router as ctime_router
from modules.upload import router as upload_router
from modules.update import router as update_router


def register_all_modules(dp: Dispatcher):
    """Register all command modules."""
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(daily_router)
    dp.include_router(weekly_router)
    dp.include_router(pay_router)
    dp.include_router(ping_router)
    dp.include_router(kill_router)
    dp.include_router(harem_router)
    dp.include_router(guess_router)
    dp.include_router(claim_router)
    dp.include_router(gift_router)
    dp.include_router(check_router)
    dp.include_router(search_router)
    dp.include_router(rarity_router)
    dp.include_router(total_router)
    dp.include_router(broadcast_router)
    dp.include_router(ctime_router)
    dp.include_router(upload_router)
    dp.include_router(update_router)

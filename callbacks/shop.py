from aiogram import Router
from modules.shop import shop_next, shop_prev, shop_buy, shop_noop

router = Router(name="shop_callbacks")

router.callback_query(shop_next)
router.callback_query(shop_prev)
router.callback_query(shop_buy)
router.callback_query(shop_noop)

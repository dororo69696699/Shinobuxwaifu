from aiogram import Router
from modules.mines import handle_mine_click, handle_claim

router = Router(name="mines_callbacks")

router.callback_query(handle_mine_click)
router.callback_query(handle_claim)

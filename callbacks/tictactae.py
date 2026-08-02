from aiogram import Router
from modules.tictactoe import (
    join_ox_callback, cancel_ox_callback, play_ox_callback
)

router = Router(name="tictactoe_callbacks")

router.callback_query(join_ox_callback)
router.callback_query(cancel_ox_callback)
router.callback_query(play_ox_callback)

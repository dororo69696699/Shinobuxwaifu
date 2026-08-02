
import time
from typing import Dict

_cooldowns: Dict[str, float] = {}


def check_cooldown(user_id: int, command: str, delay: int = 2) -> bool:
    key = f"{user_id}:{command}"
    now = time.time()
    
    if key in _cooldowns:
        if now - _cooldowns[key] < delay:
            return False
    
    _cooldowns[key] = now
    return True


def reset_cooldown(user_id: int, command: str) -> None:
    key = f"{user_id}:{command}"
    if key in _cooldowns:
        del _cooldowns[key]

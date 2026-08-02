
import html


def format_number(num: int) -> str:
    return f"{num:,}"


def get_mention(user_id: int, name: str) -> str:
    return f"<a href='tg://user?id={user_id}'>{html.escape(name)}</a>"

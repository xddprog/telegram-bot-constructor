from schemas import DialogModel
from constructors.bot_constructor import BotConstructor


async def get_bot_constructor(dialogs: list[DialogModel]) -> BotConstructor:
    return BotConstructor(
        config={"token": "BOT_TOKEN"},
        dialogs=dialogs,
    )

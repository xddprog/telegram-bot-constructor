from typing import Annotated
from fastapi import Depends, FastAPI

from constructors.bot_constructor import BotConstructor
from utils.dependencies import get_bot_constructor
from schemas import DialogModel


app = FastAPI()


@app.post("/generate/dialog")
async def generate(
    dialogs: list[DialogModel],
    constructor: Annotated[BotConstructor, Depends(get_bot_constructor)],
) -> None:
    constructor()
    return True

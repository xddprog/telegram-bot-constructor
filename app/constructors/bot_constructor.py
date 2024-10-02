import logging
from mailbox import Message
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram_dialog import Dialog, setup_dialogs

from constructors.dialog_constructor import DialogConstructor
from schemas import DialogModel


class BotConstructor:
    def __init__(
        self,
        config: dict,
        dialogs: list[DialogModel],
    ) -> None:
        self.__bot = Bot(
            **config, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.__dialogs = self._generate_dialogs(dialogs)
        self.__dispatcher = Dispatcher()

    def _generate_dialogs(self, dialogs: list[DialogModel]) -> list[DialogConstructor]:
        return [DialogConstructor(dialog) for dialog in dialogs]
    
    @staticmethod
    async def test_handler(message: Message) -> None:
        await message.answer("test")

    async def __call__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(filename)s:%(lineno)d #%(levelname)-8s "
            "[%(asctime)s] - %(name)s - %(message)s",
        )
        setup_dialogs(self.__dispatcher)

        for dialog in self.__dialogs:
            self.__dispatcher.message.register(dialog._trigger,)
            self.__dispatcher.include_router(dialog())

        await self.__dispatcher.start_polling(self.__bot)

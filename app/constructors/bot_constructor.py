import logging
from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from constructors.dialog_constructor import DialogConstructor
from schemas import DialogModel


class BotConstructor:
    def __init__(
        self,
        config: dict,
        dialogs: list[DialogModel],
    ) -> None:
        # self.__bot = Bot(
        #     **config, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        # )
        self._dialogs = self._generate_dialogs(dialogs)
        self.__dispatcher = Dispatcher()

    def _generate_dialogs(self, dialogs: list[DialogModel]) -> None:
        return [DialogConstructor(dialog)() for dialog in dialogs]

    async def __call__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(filename)s:%(lineno)d #%(levelname)-8s "
            "[%(asctime)s] - %(name)s - %(message)s",
        )
        setup_dialogs(self.__dispatcher)

        # await self.__dispatcher.start_polling(self.__bot)

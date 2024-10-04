import logging
from textwrap import dedent
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

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
    
    def __call__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(filename)s:%(lineno)d #%(levelname)-8s "
            "[%(asctime)s] -  %(name)s - %(message)s",
        )

        setup_dialogs(self.__dispatcher)
        
        dialogs = []
        triggers = []
        triggers_names = []
        states = []
        handlers = []

        for dialog in self.__dialogs:
            dialogs.append(dialog())
            triggers.append(dialog._trigger)
            states.append(dialog._states_string)
            triggers_names.append(dialog._trigger_name)

            for window in dialog._windows:
                handlers.extend(window._handlers)

        with open("test.py", "w") as file:
            file.write(
                dedent(
                    """
                        import logging
                        import asyncio
                        from aiogram import Bot, Dispatcher
                        from aiogram.client.default import DefaultBotProperties
                        from aiogram.enums import ParseMode
                        from aiogram.fsm.state import State, StatesGroup
                        from aiogram.types import CallbackQuery, Message
                        from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
                        from aiogram_dialog.widgets.kbd import Button, Column
                        from aiogram_dialog.widgets.text import Format
                    """
                )
            )

            file.write('\n'.join(states))
            file.write('\n'.join(triggers))
            file.write('\n'.join(handlers))
            file.write(f'triggers = [{",".join(triggers_names)}]\n')
            file.write(f'dialogs = [{','.join(dialogs)}]')
            file.write(
                dedent(
                    f'''
                        async def main():
                            logging.basicConfig(
                                level=logging.INFO,
                                format="%(filename)s:%(lineno)d #%(levelname)-8s "
                                "[%(asctime)s] - %(name)s - %(message)s",
                            )
                            bot = Bot(token="7589331534:AAHUwP70EtuuSOTfPWpJ2193G9IrotACOQY")
                            dp = Dispatcher()
                            for dialog in dialogs:
                                dp.include_router(dialog)
                            for trigger in triggers:
                                dp.message.register(trigger)
                            setup_dialogs(dp)
                            await dp.start_polling(bot)

                        asyncio.run(main())
                    '''
                )
            )
            

        # await self.__dispatcher.start_polling(self.__bot)

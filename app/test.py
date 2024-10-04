
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

class stringStates(StatesGroup):
    string_1 = State()
    string_2 = State()
    string_3 = State()

async def trigger_string(
    message: Message, dialog_manager: DialogManager
) -> None:
    await message.answer("test")
    await dialog_manager.start(
        stringStates.string_1, mode=StartMode.RESET_STACK
    )

async def go_to_string_string_1(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(stringStates.string_1)


async def go_to_string_string_1(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(stringStates.string_1)


async def go_to_string_string_2(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(stringStates.string_2)


async def go_to_string_string_2(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(stringStates.string_2)


async def go_to_string_string_1(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(stringStates.string_1)


async def go_to_string_string_1(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(stringStates.string_1)
triggers = [trigger_string]
dialogs = [Dialog(Window(Format('string'), Column(Column(Button(text=Format('string'),id='string_1', on_click=go_to_string_string_1)),Column(Button(text=Format('string'),id='string_1', on_click=go_to_string_string_1))), state=stringStates.string_1),Window(Format('string'), Column(Column(Button(text=Format('string'),id='string_2', on_click=go_to_string_string_2)),Column(Button(text=Format('string'),id='string_2', on_click=go_to_string_string_2))), state=stringStates.string_2),Window(Format('string'), Column(Column(Button(text=Format('string'),id='string_1', on_click=go_to_string_string_1)),Column(Button(text=Format('string'),id='string_1', on_click=go_to_string_string_1))), state=stringStates.string_3))]
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

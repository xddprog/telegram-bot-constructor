from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.button import OnClick


class HandlerConstructor:
    def _get_go_to_handler(self, switch_state: State) -> OnClick:
        async def go_to_handler(
            callback: CallbackQuery,
            button: Button,
            dialog_manager: DialogManager,
        ) -> None:
            await dialog_manager.switch_to(switch_state)

        return go_to_handler

    def __call__(self, state: State) -> OnClick:
        return self._get_go_to_handler(state)

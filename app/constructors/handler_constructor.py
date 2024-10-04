from textwrap import dedent
from aiogram.fsm.state import State
from aiogram_dialog.widgets.kbd.button import OnClick


class HandlerConstructor:
    def __init__(self, dialog_name: str, states_group_name: str) -> None:
        self.dialog_name = dialog_name
        self.states_group_name = states_group_name

    def _get_go_to_handler(self, switch_state: str) -> tuple:
        handler_name = f"go_to_{self.dialog_name}_{switch_state}"

        handler = dedent(f"""
            async def {handler_name}(
                callback: CallbackQuery,
                button: Button,
                dialog_manager: DialogManager,
            ) -> None:
                await dialog_manager.switch_to({self.states_group_name}.{switch_state})
            """)

        return handler, handler_name

    def __call__(self, state: State) -> OnClick:
        return self._get_go_to_handler(state)

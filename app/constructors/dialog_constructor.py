from textwrap import dedent
from typing import Awaitable, Callable
from aiogram_dialog import Dialog
from aiogram.fsm.state import StatesGroup, State
from constructors.window_constructor import WindowConstructor
from schemas import DialogModel


class DialogConstructor:
    def __init__(self, dialog: DialogModel) -> None:
        self._name = dialog.name
        self.__dialog = dialog
        self._states, self._states_string = self._generate_states()
        self._trigger, self._trigger_name = self._generate_trigger()
        self._windows = self._generate_windows()

    def _generate_trigger(self) -> Callable[..., Awaitable]:
        state_name = f"{self._name}States.{self._states.__states__[0]._state}"
        return dedent(f"""
            async def trigger_{self._name}(
                message: Message, dialog_manager: DialogManager
            ) -> None:
                await message.answer("test")
                await dialog_manager.start(
                    {state_name}, mode=StartMode.RESET_STACK
                )
        """), f'trigger_{self._name}'

    def _generate_states(self) -> StatesGroup:
        class DialogStates(StatesGroup):
            pass

        for index in range(len(self.__dialog.windows)):
            state_name = f"{self._name}_{index + 1}"

            setattr(DialogStates, state_name, State(state=state_name))

            DialogStates.__dict__[state_name].set_parent(DialogStates)
            DialogStates.__states__ += (DialogStates.__dict__[state_name],)

        return (
            DialogStates, 
            dedent(
            f"""\nclass {self._name}States(StatesGroup):
    {'\n    '.join([f'{self._name}_{index + 1} = State()' for index in range(len(self.__dialog.windows))])}
            """)
        )
    
    def _generate_windows(self) -> list[str]:
        return [
            WindowConstructor(window, self._states, state, self._name)
            for window, state in zip(self.__dialog.windows, self._states.__states__)
        ]

    def __call__(self) -> Dialog:
        return f"Dialog({','.join(window() for window in self._windows)})"

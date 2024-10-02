from aiogram_dialog import Dialog
from aiogram.fsm.state import StatesGroup, State
from constructors.window_constructor import WindowConstructor
from schemas import DialogModel


class DialogConstructor:
    def __init__(self, dialog: DialogModel) -> None:
        self.__dialog = dialog
        self._states = self._generate_states()

    def _generate_states(self) -> StatesGroup:
        class DialogStates(StatesGroup):
            pass

        for index in range(10):
            state_name = f"{self.__dialog.name}_{index}"
            setattr(DialogStates, state_name, State(state=state_name))
            DialogStates.__dict__[state_name].set_parent(DialogStates)
            DialogStates.__states__ += (DialogStates.__dict__[state_name],)

        return DialogStates

    def __call__(self) -> Dialog:
        windows = [
            WindowConstructor(window, self._states, state=state)()
            for window, state in zip(
                self.__dialog.windows, self._states.__states__
            )
        ]
        return Dialog(*windows, name=self.__dialog.name)

from textwrap import dedent
from typing import Awaitable
from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.api.internal import DataGetter
from aiogram_dialog.widgets.kbd import Button, Column, Row
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from constructors.handler_constructor import HandlerConstructor
from schemas import (
    ButtonModel,
    ColumnButtonsModel,
    KeyboardModel,
    RowButtonsModel,
    TextModel,
    WindowModel,
)


class WindowConstructor:
    def __init__(
        self,
        window: WindowModel,
        states: list[State],
        state: State,
        dialog_name: str,
    ) -> None:
        self.__window = window
        self._getters = []
        self._handlers = []
        self._state = state
        self._states = states
        self.dialog_name = dialog_name
        self.handler_constructor = HandlerConstructor(
            self.dialog_name, f'{self.dialog_name}States'
        )

    def _generate_handler(self, next_state: str) -> Awaitable:
        return self.handler_constructor(next_state)

    def get_state_with_name(self, state_name: str) -> State:
        return getattr(self._states, state_name)

    def _generate_text(self, text_model: TextModel) -> Const | Format:
        if text_model.type == "const":
            return f"Const('{text_model.text}')"
        else:
            return f"Format('{text_model.text}')"

    def _generate_getter(self) -> DataGetter:
        pass

    def _generate_button(self, button: ButtonModel) -> Button:
        handler, handler_name = None, None

        if button.next_window:
            handler, handler_name = self._generate_handler(button.next_window)
            self._handlers.append(handler)

        return dedent(
            f"Button(text={self._generate_text(button.text)},id='{button.next_window if button.next_window else handler_name}', on_click={handler_name})"
        )

    def _generate_buttons_row(self, row: RowButtonsModel) -> Row:
        return dedent(
            f"""Row({','.join([self._generate_button(button) for button in row.buttons])})"""
        )

    def _generate_buttons_column(self, column: ColumnButtonsModel) -> Column:
        return dedent(
            f"""Column({','.join([self._generate_button(row) for row in column.buttons])})"""
        )

    def _generate_keyboard(self, keyboard: KeyboardModel) -> Column:
        rows_and_columns = []

        for item in keyboard.rows_and_columns:
            if isinstance(item, ColumnButtonsModel):
                rows_and_columns.append(self._generate_buttons_column(item))
            else:
                rows_and_columns.append(self._generate_buttons_row(item))

        return dedent(f"""Column({','.join(rows_and_columns)})""")

    def _generate_media(self) -> DynamicMedia | StaticMedia:
        pass

    def __call__(self) -> Window:
        keyboard = self._generate_keyboard(self.__window.keyboard)
        text = self._generate_text(self.__window.text)
        return dedent(f"""Window({text}, {keyboard}, state={self.dialog_name}States.{self.__window.state})""")

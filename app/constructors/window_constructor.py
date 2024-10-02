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
        self, window: WindowModel, states: list[State], state: State
    ) -> None:
        self.__window = window
        self._getters = []
        self._handlers = []
        self._state = state
        self._states = states
        self.handler_constructor = HandlerConstructor()

    @property
    def get_getters(self) -> State:
        return self._getters

    @property
    def get_handlers(self) -> State:
        return self._handlers

    def get_state_with_name(self, state_name: str) -> State:
        return getattr(self._states, state_name)

    def _generate_text(self, text_model: TextModel) -> Const | Format:
        if text_model.type == "const":
            return Const(text_model.text)
        else:
            return Format(text_model.text)

    def _generate_getter(self) -> DataGetter:
        pass

    def _generate_button(self, button: ButtonModel) -> Button:
        return Button(
            id="id",
            text=self._generate_text(button.text),
            on_click=self._generate_handler(button.next_window),
        )

    def _generate_buttons_row(self, row: RowButtonsModel) -> Row:
        return Row(*[self._generate_button(button) for button in row.buttons])

    def _generate_buttons_column(self, column: ColumnButtonsModel) -> Column:
        return Column(*[self._generate_button(row) for row in column.buttons])

    def _generate_keyboard(self, keyboard: KeyboardModel) -> Column:
        rows_and_columns = []

        for item in keyboard.rows_and_columns:
            if isinstance(item, ColumnButtonsModel):
                rows_and_columns.append(self._generate_buttons_column(item))
            else:
                rows_and_columns.append(self._generate_buttons_row(item))
        print(rows_and_columns)
        return Column(*rows_and_columns)

    def _generate_media(self) -> DynamicMedia | StaticMedia:
        pass

    def _generate_handler(self, next_state: str) -> Awaitable:
        next_state = self.get_state_with_name(next_state)
        return self.handler_constructor(next_state)

    def __call__(self) -> Window:
        keyboard = self._generate_keyboard(self.__window.keyboard)
        text = self._generate_text(self.__window.text)
        return Window(text, keyboard, state=self._state)

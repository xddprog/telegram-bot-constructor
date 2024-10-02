from fastapi import UploadFile
from pydantic import BaseModel, Field


class TextModel(BaseModel):
    text: str
    type: str


class ButtonModel(BaseModel):
    text: TextModel
    next_window: str = Field(examples=["string_1"])


class RowButtonsModel(BaseModel):
    buttons: list[ButtonModel]


class ColumnButtonsModel(BaseModel):
    buttons: list[ButtonModel]


class KeyboardModel(BaseModel):
    rows_and_columns: list[ColumnButtonsModel | RowButtonsModel]


class WindowModel(BaseModel):
    text: TextModel | None = None
    files: list[UploadFile] | None = None
    state: str
    keyboard: KeyboardModel | None = None


class DialogModel(BaseModel):
    name: str
    windows: list[WindowModel]

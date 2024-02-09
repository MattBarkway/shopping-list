import datetime
from typing import Any

from pydantic import BaseModel, validator, model_validator


class CreatedResponse(BaseModel):
    id: int


class CreateItem(BaseModel):
    name: str
    description: str
    quantity: int


class UpdateItem(BaseModel):
    name: str | None
    description: str | None
    quantity: int | None

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert "card_number" not in data, "card_number should not be included"
        return data


class ExistingItem(CreateItem, CreatedResponse): ...


class CreateShoppingList(BaseModel):
    name: str


class UpdateShoppingList(BaseModel):
    name: str | None


class ExistingShoppingList(CreateShoppingList, CreatedResponse):
    owner: str
    last_updated: datetime.datetime


class CreateCollaborator(BaseModel):
    user_id: int | None
    email: str | None

    @validator("user_id", "email", pre=True, always=True)
    def check_fields(cls, v, values):
        if "user_id" in values and "email" in values:
            if v is None and values["email"] is None:
                raise ValueError(
                    "Both user_id and email cannot be None at the same time"
                )
        return v


class ExistingCollaborator(CreatedResponse, CreateCollaborator): ...

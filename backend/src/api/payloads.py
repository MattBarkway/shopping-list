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
    name: str | None = None
    description: str | None = None
    quantity: int | None = None

    @model_validator(mode="before")
    @classmethod
    def check_fields(cls, data: Any) -> Any:
        if not any(data.get(i) for i in ["name", "description", "quantity"]):
            raise ValueError("name, description and quantity cannot all be empty")
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
    user_id: int | None = None
    email: str | None = None

    @model_validator(mode="before")
    @classmethod
    def check_fields(cls, data: Any):
        if not any(data.get(i) for i in ["user_id", "email"]):
            raise ValueError("User and email cannot both be empty")
        return data


class ExistingCollaborator(CreatedResponse, CreateCollaborator):
    ...


class UserInfo(BaseModel):
    username: str

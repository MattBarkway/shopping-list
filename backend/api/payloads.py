from pydantic import BaseModel


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


class ExistingItem(CreateItem, CreatedResponse):
    ...


class CreateShoppingList(BaseModel):
    name: str


class UpdateShoppingList(BaseModel):
    name: str | None


class ExistingShoppingList(CreateShoppingList, CreatedResponse):
    owner: str


class CreateCollaborator(BaseModel):
    user_id: int


class ExistingCollaborator(CreatedResponse, CreateCollaborator):
    username: str

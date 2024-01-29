from datetime import datetime
from typing import ClassVar

from sqlalchemy import ForeignKey, String, JSON, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class SLBase(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    def to_dict(self):
        out = self.__dict__.copy()
        del out["_sa_instance_state"]

        return out


class User(SLBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(256), unique=True)
    pw_hash: Mapped[str] = mapped_column(String(256))
    salt: Mapped[str] = mapped_column(String(256))
    verified: Mapped[bool] = mapped_column(default=False)

    lists: Mapped[list["ShoppingList"]] = relationship(back_populates="owner")


class Collaborator(SLBase):
    __tablename__ = "collaborator"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    list_id: Mapped[int] = mapped_column(ForeignKey("shopping_list.id"))

    list: Mapped["ShoppingList"] = relationship(back_populates="collaborators")


class ShoppingList(SLBase):
    __tablename__ = "shopping_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(256))

    owner: Mapped["User"] = relationship(back_populates="lists", lazy="joined")
    collaborators: Mapped[list["Collaborator"]] = relationship(back_populates="list")
    items: Mapped[list["Item"]] = relationship(back_populates="shopping_list")


class Item(SLBase):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    sl_id: Mapped[int] = mapped_column(ForeignKey("shopping_list.id"))

    name: Mapped[str]
    description: Mapped[str]
    quantity: Mapped[int]

    shopping_list: Mapped["ShoppingList"] = relationship(
        back_populates="items", lazy="joined"
    )

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=200))
    hashed_password: Mapped[str] = mapped_column(String(length=200))
    first_name: Mapped[str] = mapped_column(String(length=100))
    last_name: Mapped[str] = mapped_column(String(length=100))
    nick_name: Mapped[str] = mapped_column(String(length=100))
    number: Mapped[str | None] = mapped_column(String(length=100))

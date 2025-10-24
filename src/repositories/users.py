from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemes.users import User


class UsersRepository(BaseRepository):
    model = UsersORM
    scheme = User

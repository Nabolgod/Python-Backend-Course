from src.repositories.mappers.base import DataMapper

from src.schemes.hotels import Hotel
from src.models.hotels import HotelsORM

from src.schemes.rooms import Room, RoomWithRels
from src.models.rooms import RoomsORM

from src.schemes.bookings import Booking
from src.models.bookings import BookingsORM

from src.schemes.users import User
from src.models.users import UsersORM

from src.schemes.facilities import Facility, RoomFacility
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM


class HotelsDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class RoomsWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class BookingsDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class UsersDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ..repositories.repositories import RoomRepository, BookingRepository
from ..serializers.serializers import RoomSerializer, BookingSerializer


class RoomService:
    @staticmethod
    def create_room(data: dict):
        """Создание комнаты (бизнес-логика)"""
        validated_data = RoomSerializer.validate_room_data(data)
        return RoomRepository.create_room(
            description=validated_data["description"],
            price_per_night=validated_data["price_per_night"]
        )
    
    @staticmethod
    def get_rooms_list(sort_by: str, order: str):
        """Получение списка комнат"""
        return RoomRepository.get_all_rooms(sort_by, order)

    @staticmethod
    def delete_room(room_id: int):
        """Удаление комнаты"""
        RoomRepository.delete_room(room_id)

class BookingService:
    @staticmethod
    def create_booking(data: dict):
        """Создание бронирования (бизнес-логика)"""
        validated_data = BookingSerializer.validate_booking_data(data)

        if BookingRepository.check_booking_conflict(
            validated_data["room_id"],
            validated_data["start_date"],
            validated_data["end_date"]
        ):
            raise ValidationError("Room already booked for these dates")
        
        return BookingRepository.create_booking(
            room_id=validated_data["room_id"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"]
        )
    
    @staticmethod
    def get_bookings_by_room(room_id: int):
        """Получение бронирований по комнате"""
        if not RoomRepository.room_exists(room_id):
            raise ObjectDoesNotExist("Room not found")
        return BookingRepository.get_bookings_by_room(room_id)
    
    @staticmethod
    def delete_booking(booking_id: int):
        """Удаление бронирования"""
        BookingRepository.delete_booking(booking_id)
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ..models.models import Room, Booking


class RoomRepository:
    @staticmethod
    def get_room(room_id: int) -> Room:
        """Получить комнату по ID"""
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise ObjectDoesNotExist("Room not found")
    
    @staticmethod
    def get_all_rooms(sort_by: str = "id", order: str = "asc") -> list[Room]:
        """Получить все комнаты с сортировкой"""
        sort_mapping = {
            "price": "price_per_night",
            "date": "created_at", 
            "id": "id"
        }
        
        sort_field = sort_mapping.get(sort_by, "id")
        if order == "desc":
            sort_field = "-" + sort_field
        
        return Room.objects.all().order_by(sort_field)
    
    @staticmethod
    def create_room(description: str, price_per_night: str) -> Room:
        """Создать новую комнату"""
        room = Room(description=description, price_per_night=price_per_night)
        room.full_clean()
        room.save()
        return room
    
    @staticmethod
    def delete_room(room_id: int) -> None:
        """Удалить комнату"""
        room = RoomRepository.get_room(room_id)
        room.delete()

    @staticmethod
    def room_exists(room_id: int) -> bool:
        """Проверить существование комнаты"""
        return Room.objects.filter(id=room_id).exists()
    

class BookingRepository:
    @staticmethod
    def get_booking(booking_id: int) -> Booking:
        """Получить бронирование по ID"""
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise ObjectDoesNotExist("Booking not found")
    
    @staticmethod
    def get_bookings_by_room(room_id: int) -> list[Booking]:
        """Получить все бронирования для комнаты"""
        return Booking.objects.filter(room_id=room_id).order_by("start_date")
    
    @staticmethod
    def check_booking_conflict(room_id: int, start_date, end_date) -> bool:
        """Проверить конфликт бронирований"""
        existing_bookings = Booking.objects.filter(
            room_id=room_id,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        return existing_bookings.exists()
    
    @staticmethod
    def create_booking(room_id: int, start_date, end_date) -> Booking:
        """Создать новое бронирование"""
        room = RoomRepository.get_room(room_id)               
        booking = Booking(room=room, start_date=start_date, end_date=end_date)
        booking.full_clean()
        booking.save()
        return booking
    
    
    @staticmethod
    def delete_booking(booking_id: int) -> None:
        """Удалить бронирование"""
        booking = BookingRepository.get_booking(booking_id)
        booking.delete()
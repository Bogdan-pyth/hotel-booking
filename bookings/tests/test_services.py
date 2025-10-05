from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from datetime import date, timedelta
from ..models.models import Room, Booking
from ..services.services import RoomService, BookingService


class RoomServiceTest(TestCase):
    
    def setUp(self):
        self.room_data = {
            "description": "Тестовый номер",
            "price_per_night": "10000.00"
        }
    
    def test_create_room_success(self):
        room = RoomService.create_room(self.room_data)
        
        self.assertIsInstance(room, Room)
        self.assertEqual(room.description, "Тестовый номер")
        self.assertEqual(str(room.price_per_night), "10000.00")
        self.assertEqual(Room.objects.count(), 1)
    
    def test_create_room_invalid_data(self):
        invalid_data = {
            "description": "Тестовый номер",
            "price_per_night": "-100.00" 
        }
        
        with self.assertRaises(ValidationError):
            RoomService.create_room(invalid_data)
    
    def test_get_rooms_list(self):
        Room.objects.create(description="Дорогой", price_per_night="20000.00")
        Room.objects.create(description="Дешёвый", price_per_night="5000.00")
        
        rooms = RoomService.get_rooms_list("price", "desc")
        
        self.assertEqual(len(rooms), 2)
        self.assertEqual(rooms[0].price_per_night, 20000.00)
        self.assertEqual(rooms[1].price_per_night, 5000.00)
    
    def test_delete_room_success(self):
        """Тестируем удаление комнаты через сервис"""
        room = Room.objects.create(description="Тест", price_per_night="1000.00")
        
        RoomService.delete_room(room.id)
        
        self.assertEqual(Room.objects.count(), 0)
    
    def test_delete_nonexistent_room(self):
        with self.assertRaises(ObjectDoesNotExist):
            RoomService.delete_room(999)


class BookingServiceTest(TestCase):
    """Тесты для BookingService"""
    
    def setUp(self):
        self.room = Room.objects.create(
            description="Тестовый номер",
            price_per_night="10000.00"
        )
        
        self.booking_data = {
            "room_id": self.room.id,
            "start_date": (date.today() + timedelta(days=5)).isoformat(),
            "end_date": (date.today() + timedelta(days=10)).isoformat()
        }
    
    def test_create_booking_success(self):
        booking = BookingService.create_booking(self.booking_data)
        
        self.assertIsInstance(booking, Booking)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_create_booking_room_not_found(self):
        invalid_data = {
            "room_id": 999,
            "start_date": (date.today() + timedelta(days=5)).isoformat(),
            "end_date": (date.today() + timedelta(days=10)).isoformat()
        }
        
        with self.assertRaises(ObjectDoesNotExist):
            BookingService.create_booking(invalid_data)
    
    def test_create_booking_date_conflict(self):
        Booking.objects.create(
            room=self.room,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=10)
        )
        
        with self.assertRaises(ValidationError) as context:
            BookingService.create_booking(self.booking_data)
        
        self.assertIn("already booked", str(context.exception))
    
    def test_get_bookings_by_room(self):
        booking1 = Booking.objects.create(
            room=self.room,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3)
        )
        
        booking2 = Booking.objects.create(
            room=self.room,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12)
        )
        
        bookings = BookingService.get_bookings_by_room(self.room.id)
        
        self.assertEqual(len(bookings), 2)
        self.assertIn(booking1, bookings)
        self.assertIn(booking2, bookings)
    
    def test_get_bookings_nonexistent_room(self):
        with self.assertRaises(ObjectDoesNotExist):
            BookingService.get_bookings_by_room(999)
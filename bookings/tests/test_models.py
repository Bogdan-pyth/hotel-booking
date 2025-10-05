from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from ..models.models import Room, Booking


class RoomModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room = Room.objects.create(
            description = "Уютный номер с видом на море",
            price_per_night = "15000.00"
        )
            
    def test_room_creation(self):
        self.assertEqual(self.room.description, "Уютный номер с видом на море")
        self.assertEqual(str(self.room.price_per_night), "15000.00")
        self.assertIsNotNone(self.room.created_at)

    def test_room_string_representation(self):
        expected_str = f"Room {self.room.id}: {self.room.description[:50]}"
        self.assertEqual(str(self.room), expected_str)
    
    def test_room_description_required(self):
        room = Room(price_per_night="1000.00")  
        
        with self.assertRaises(ValidationError):
            room.full_clean()

class BookingModelTest(TestCase):
        
    @classmethod
    def setUpTestData(cls):
        cls.room = Room.objects.create(
            description="Тестовый номер для бронирования",
            price_per_night="12000.00"
        )
        
        cls.booking = Booking.objects.create(
            room=cls.room,
            start_date=date(2024, 1, 15),
            end_date=date(2024, 1, 20)
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.room, self.room)
        self.assertEqual(self.booking.start_date, date(2024, 1, 15))
        self.assertEqual(self.booking.end_date, date(2024, 1, 20))
    
    def test_booking_string_representation(self):
        expected_str = f"Booking {self.booking.id} for room {self.room.id} (2024-01-15 to 2024-01-20)"
        self.assertEqual(str(self.booking), expected_str)
        
    def test_booking_room_required(self):
        booking = Booking(
            start_date=date(2024, 1, 15),
            end_date=date(2024, 1, 20)
        )
        
        with self.assertRaises(ValidationError):
            booking.full_clean()
    
    def test_booking_duration_calculation(self):
        booking = Booking(
            room=self.room,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 5)
        )
        booking.save()
        
        duration = (booking.end_date - booking.start_date).days
        self.assertEqual(duration, 4)

class RoomBookingRelationshipTest(TestCase):
    
    def test_room_booking_relationship(self):
        room = Room.objects.create(
            description="Номер для тестирования связей",
            price_per_night="10000.00"
        )
        
        booking1 = Booking.objects.create(
            room=room,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 3)
        )
        
        booking2 = Booking.objects.create(
            room=room,
            start_date=date(2024, 1, 10),
            end_date=date(2024, 1, 12)
        )
        
        self.assertEqual(booking1.room, room)
        self.assertEqual(booking2.room, room)
        
        room_bookings = room.bookings.all()
        self.assertEqual(room_bookings.count(), 2)
        self.assertIn(booking1, room_bookings)
        self.assertIn(booking2, room_bookings)
    
    def test_room_deletion_cascades(self):
        room = Room.objects.create(
            description="Комната для удаления",
            price_per_night="8000.00"
        )
        
        booking = Booking.objects.create(
            room=room,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 3)
        )
        
        self.assertEqual(Booking.objects.count(), 1)
        
        room.delete()
        
        self.assertEqual(Booking.objects.count(), 0)
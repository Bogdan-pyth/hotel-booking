from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from ..serializers.serializers import RoomSerializer, BookingSerializer


class RoomSerializerTest(TestCase):
    
    def test_valid_room_data(self):
        data = {
            "description": "Тестовый номер",
            "price_per_night": "15000.00"
        }
        
        validated_data = RoomSerializer.validate_room_data(data)
        self.assertEqual(validated_data["description"], "Тестовый номер")
        self.assertEqual(validated_data["price_per_night"], "15000.00")
    
    def test_room_negative_price_validation(self):
        data = {
            "description": "Тестовый номер",
            "price_per_night": "-100.00"
        }
        
        with self.assertRaises(ValidationError) as context:
            RoomSerializer.validate_room_data(data)
        
        self.assertIn("price_per_night must be positive", str(context.exception))
    
    def test_room_zero_price_validation(self):
        data = {
            "description": "Тестовый номер",
            "price_per_night": "0.00"
        }
        
        with self.assertRaises(ValidationError) as context:
            RoomSerializer.validate_room_data(data)
        
        self.assertIn("price_per_night must be positive", str(context.exception))
    
    def test_room_missing_description(self):
        data = {
            "price_per_night": "10000.00"
        }
        
        with self.assertRaises(ValidationError) as context:
            RoomSerializer.validate_room_data(data)
        
        self.assertIn("description is required", str(context.exception))
    
    def test_room_missing_price(self):
        data = {
            "description": "Тестовый номер"
        }
        
        with self.assertRaises(ValidationError) as context:
            RoomSerializer.validate_room_data(data)
        
        self.assertIn("price_per_night is required", str(context.exception))


class BookingSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.today = date.today()
        cls.future_date = cls.today + timedelta(days=10)
        cls.future_date_plus = cls.today + timedelta(days=15)
        cls.past_date = cls.today - timedelta(days=1)
    
    def test_valid_booking_data(self):
        data = {
            "room_id": 1,
            "start_date": self.future_date.isoformat(),
            "end_date": self.future_date_plus.isoformat()
        }
        
        validated_data = BookingSerializer.validate_booking_data(data)
        self.assertEqual(validated_data["room_id"], 1)
        self.assertEqual(validated_data["start_date"], self.future_date)
        self.assertEqual(validated_data["end_date"], self.future_date_plus)
    
    def test_booking_invalid_dates_validation(self):
        data = {
            "room_id": 1,
            "start_date": self.future_date_plus.isoformat(),
            "end_date": self.future_date.isoformat()
        }
        
        with self.assertRaises(ValidationError) as context:
            BookingSerializer.validate_booking_data(data)
        
        self.assertIn("end_date must be after start_date", str(context.exception))
    
    def test_booking_same_dates_validation(self):
        data = {
            "room_id": 1,
            "start_date": self.today.isoformat(),
            "end_date": self.today.isoformat()
        }
        
        with self.assertRaises(ValidationError) as context:
            BookingSerializer.validate_booking_data(data)
        
        self.assertIn("end_date must be after start_date", str(context.exception))
    
    def test_booking_past_dates_validation(self):
        data = {
            "room_id": 1,
            "start_date": self.past_date.isoformat(),
            "end_date": self.future_date.isoformat()
        }
        
        with self.assertRaises(ValidationError) as context:
            BookingSerializer.validate_booking_data(data)
        
        self.assertIn("Cannot book in the past", str(context.exception))
    
    def test_booking_invalid_date_format(self):
        data = {
            "room_id": 1,
            "start_date": "1991/12/21",
            "end_date": self.future_date.isoformat()
        }
        
        with self.assertRaises(ValidationError) as context:
            BookingSerializer.validate_booking_data(data)
        
        self.assertIn("Invalid date format", str(context.exception))
    
    def test_booking_missing_room_id(self):
        data = {
            "start_date": self.future_date.isoformat(),
            "end_date": self.future_date_plus.isoformat()
        }
        
        with self.assertRaises(ValidationError) as context:
            BookingSerializer.validate_booking_data(data)
        
        self.assertIn("room_id is required", str(context.exception))
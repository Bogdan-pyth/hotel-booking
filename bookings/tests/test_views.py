from django.test import TestCase
from django.urls import reverse
import json
from ..models.models import Room, Booking
from datetime import date, timedelta


class RoomAPITest(TestCase):
    
    def setUp(self):
        self.room = Room.objects.create(
            description="Тестовый номер",
            price_per_night="10000.00"
        )
        self.room_data = {
            "description": "Новый номер",
            "price_per_night": "15000.00"
        }
    
    def test_get_rooms_list(self):
        response = self.client.get('/rooms/list')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['description'], "Тестовый номер")
    
    def test_create_room_success(self):
        response = self.client.post(
            '/rooms/add',
            data=json.dumps(self.room_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        
        self.assertEqual(Room.objects.count(), 2)
    
    def test_create_room_invalid_data(self):
        invalid_data = {
            "description": "Новый номер",
            "price_per_night": "-100.00"
        }
        
        response = self.client.post(
            '/rooms/add',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
    
    def test_delete_room_success(self):
        response = self.client.delete(f'/rooms/delete/{self.room.id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'deleted')
        self.assertEqual(Room.objects.count(), 0)
    
    def test_delete_nonexistent_room(self):
        response = self.client.delete('/rooms/delete/999')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())


class BookingAPITest(TestCase):
    
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
        response = self.client.post(
            '/bookings/add',
            data=json.dumps(self.booking_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_create_booking_room_not_found(self):
        invalid_data = {
            "room_id": 999,
            "start_date": (date.today() + timedelta(days=5)).isoformat(),
            "end_date": (date.today() + timedelta(days=10)).isoformat()
        }
        
        response = self.client.post(
            '/bookings/add',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())
    
    def test_get_bookings_list(self):
        Booking.objects.create(
            room=self.room,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3)
        )
        
        response = self.client.get(f'/bookings/list?room_id={self.room.id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_delete_booking_success(self):
        booking = Booking.objects.create(
            room=self.room,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3)
        )
        
        response = self.client.delete(f'/bookings/delete/{booking.id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
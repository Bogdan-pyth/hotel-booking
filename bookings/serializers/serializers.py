import json
from datetime import datetime
from typing import Any
from django.core.exceptions import ValidationError
from django.http import JsonResponse


class BookingSerializer:
    @staticmethod
    def validate_booking_data(data: dict[str, Any]) -> dict[str, Any]:
        """Валидация данных для бронирования"""
        required_fields = ["room_id", "start_date", "end_date"]
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"{field} is required")
        
        try:
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        except ValueError as e:
            raise ValidationError(f"Invalid date format: {e!s}")
        
        if start_date >= end_date:
            raise ValidationError("end_date must be after start_date")
        
        return {
            "room_id": data["room_id"],
            "start_date": start_date,
            "end_date": end_date
        }


class RoomSerializer:
    @staticmethod
    def validate_room_data(data: dict[str, Any]) -> dict[str, Any]:
        """Валидация данных для комнаты"""
        if not data.get("description"):
            raise ValidationError("description is required")
        if not data.get("price_per_night"):
            raise ValidationError("price_per_night is required")
        
        return {
            "description": data["description"],
            "price_per_night": data["price_per_night"]
        }
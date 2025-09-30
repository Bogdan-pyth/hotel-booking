import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Booking, Room

@csrf_exempt
def add_room(request: HttpRequest) -> JsonResponse:
    """rooms/add"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    if not data.get("description"):
        return JsonResponse({"error": "description is required"}, status=400)
    if not data.get("price_per_night"):
        return JsonResponse({"error": "price_per_night is required"}, status=400)
    
    room = Room(
        description=data["description"],
        price_per_night=data["price_per_night"]
    )
    
    try:
        room.full_clean() 
        room.save()

        return JsonResponse({"id": room.id}, status=201)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt   
def delete_room(request: HttpRequest, room_id: int) -> JsonResponse:
    """rooms/delete/<int:room_id>"""
    try:
        room = Room.objects.get(id=room_id)
        room.delete()
        return JsonResponse({"status": "deleted", "room_id": room_id})
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_room_list(request: HttpRequest) -> JsonResponse:
    """rooms/list"""
    sort_by = request.GET.get("sort", "id")  
    
    sort_mapping = {
        "price": "price_per_night",
        "date": "created_at", 
        "id": "id"
    }
    
    sort_field = sort_mapping.get(sort_by, "id")
    
    if request.GET.get("order") == "desc":
        sort_field = "-" + sort_field
    
    rooms = Room.objects.all().order_by(sort_field)
    
    rooms_data = []
    for room in rooms:
        rooms_data.append({
            "id": room.id,
            "description": room.description,
            "price_per_night": str(room.price_per_night), 
            "created_at": room.created_at.isoformat()
        })
    
    return JsonResponse(rooms_data, safe=False)

@csrf_exempt
def add_booking(request: HttpRequest) -> JsonResponse:
    """bookings/add"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    required_fields = ["room_id", "start_date", "end_date"]
    for field in required_fields:
        if field not in data:
            return JsonResponse({"error": f"{field} is required"}, status=400)
    
    try:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except ValueError as e:
        return JsonResponse({"error": f"Invalid date format: {e!s}"}, status=400)

    if start_date >= end_date:
        return JsonResponse({"error": "end_date must be after start_date"}, status=400)    
    
    try:  
        room = Room.objects.get(id=data["room_id"])
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    
    existing_bookings = Booking.objects.filter(
        room=room,
        start_date__lt=end_date,
        end_date__gt=start_date
    )   
    if existing_bookings.exists():
        return JsonResponse({"error": "Room already booked for these dates"}, status=400)    
         
    booking = Booking(
        room=room,
        start_date=start_date,
        end_date=end_date
    )

    try:    
        booking.full_clean()
        booking.save()
        return JsonResponse({"id": booking.id}, status=201)
    
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
def delete_booking(request: HttpRequest, booking_id: int) -> JsonResponse:
    """bookings/delete/<int:booking_id>"""
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return JsonResponse({"status": "deleted", "booking_id": booking_id})
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_booking_list(request: HttpRequest) -> JsonResponse:
    """bookings/list"""
    room_id = request.GET.get("room_id")
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    
    try:
        bookings = Booking.objects.filter(room=room).order_by("start_date")

        bookings_data = []
        for booking in bookings:
            bookings_data.append({
                "id": booking.id,
                "start_date": booking.start_date.isoformat(),
                "end_date": booking.end_date.isoformat(),
            })
        return JsonResponse(bookings_data, safe=False)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        
        
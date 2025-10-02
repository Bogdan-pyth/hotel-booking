import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ..services.services import RoomService, BookingService


@csrf_exempt
@require_http_methods(["POST"])
def add_room(request: HttpRequest) -> JsonResponse:
    """rooms/add"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    try:
        room = RoomService.create_room(data)
        return JsonResponse({"id": room.id}, status=201)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])   
def delete_room(request: HttpRequest, room_id: int) -> JsonResponse:
    """rooms/delete/<int:room_id>"""
    try:
        RoomService.delete_room(room_id)
        return JsonResponse({"status": "deleted", "room_id": room_id})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_room_list(request: HttpRequest) -> JsonResponse:
    """rooms/list"""
    try:
        sort_by = request.GET.get("sort", "id")
        order = request.GET.get("order", "asc")
        
        rooms = RoomService.get_rooms_list(sort_by, order)
        
        rooms_data = []
        for room in rooms:
            rooms_data.append({
                "id": room.id,
                "description": room.description,
                "price_per_night": str(room.price_per_night), 
                "created_at": room.created_at.isoformat()
            })
        
        return JsonResponse(rooms_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_booking(request: HttpRequest) -> JsonResponse:
    """bookings/add"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    try:
        booking = BookingService.create_booking(data)
        return JsonResponse({"id": booking.id}, status=201)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_booking(request: HttpRequest, booking_id: int) -> JsonResponse:
    """bookings/delete/<int:booking_id>"""
    try:
        BookingService.delete_booking(booking_id)
        return JsonResponse({"status": "deleted", "booking_id": booking_id})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_booking_list(request: HttpRequest) -> JsonResponse:
    """bookings/list"""
    try:
        room_id = request.GET.get("room_id")
        
        if not room_id:
            return JsonResponse({"error": "room_id parameter is required"}, status=400)
        
        bookings = BookingService.get_bookings_by_room(int(room_id))
        
        bookings_data = []
        for booking in bookings:
            bookings_data.append({
                "id": booking.id,
                "start_date": booking.start_date.isoformat(),
                "end_date": booking.end_date.isoformat(),
            })
        
        return JsonResponse(bookings_data, safe=False)
    
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
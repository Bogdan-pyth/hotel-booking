from django.db import models

class Room(models.Model):
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Room {self.id}: {self.description[:50]}"
    
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"Booking {self.id} for room {self.room_id} ({self.start_date} to {self.end_date})" 
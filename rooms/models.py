from django.db import models
from owners.models import Owner

class Room(models.Model):
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    room_number = models.CharField(max_length=20)
    rent_amount = models.PositiveIntegerField()
    location = models.CharField(max_length=150)

    image = models.ImageField(upload_to="rooms/", blank=True, null=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

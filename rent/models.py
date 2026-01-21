from django.db import models
from django.core.exceptions import ValidationError
from rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        # Basic validations
        if self.start_date >= self.end_date:
            raise ValidationError({"end_date": "End date must be after start date."})

        # Check for overlapping confirmed bookings
        overlapping = Booking.objects.filter(
            room=self.room,
            status="confirmed",
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("Room is not available for the selected dates.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} — {self.room} ({self.start_date} to {self.end_date})"

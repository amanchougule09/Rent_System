from django.db import models
from accounts.models import UserProfile
from owners.models import Owner
from rooms.models import Room

class Tenant(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenants"
    )

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    due_type = models.CharField(
        max_length=10,
        choices=(("fixed", "Fixed"), ("cycle", "Cycle"))
    )
    due_date = models.DateField(null=True, blank=True)

    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.mobile})"

from django.test import TestCase
from owners.models import Owner
from accounts.models import UserProfile
from rooms.models import Room
from .models import Booking
from datetime import date, timedelta
from django.core.exceptions import ValidationError


class BookingModelTests(TestCase):
    def setUp(self):
        self.owner_user = UserProfile.objects.create(mobile='9998887777', role='owner')
        self.owner = Owner.objects.create(user=self.owner_user, name='Owner')
        self.room = Room.objects.create(owner=self.owner, title='Test Room', room_number='101', rent_amount=1000, location='City')

    def test_overlapping_confirmed_booking_raises(self):
        b1 = Booking.objects.create(
            room=self.room,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=5),
            customer_name='A',
            customer_email='a@example.com',
            status='confirmed'
        )

        b2 = Booking(
            room=self.room,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=3),
            customer_name='B',
            customer_email='b@example.com',
            status='confirmed'
        )

        with self.assertRaises(ValidationError):
            b2.full_clean()

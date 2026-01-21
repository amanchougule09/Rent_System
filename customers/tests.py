from django.test import TestCase
from django.urls import reverse
from owners.models import Owner
from accounts.models import UserProfile
from rooms.models import Room


class CustomerViewsTests(TestCase):
    def setUp(self):
        owner_user = UserProfile.objects.create(mobile='9998887770', role='owner')
        owner = Owner.objects.create(user=owner_user, name='Owner')
        Room.objects.create(owner=owner, title='Room A', room_number='1', rent_amount=1000, location='Town')

    def test_room_list_shows_rooms(self):
        resp = self.client.get(reverse('customers:room_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Room A')

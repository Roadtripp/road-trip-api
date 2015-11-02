from django.test import TestCase
from .models import *


# Create your tests here.
class TripTestCase(TestCase):
    def setUp(self):
        test_trip = Trip.objects.create(
            pk=1,
            title="TITLE",
            origin="800 Blackwell St. Durham, NC",
            destination="New York, NY",
            start="2008-04-10 11:47:58-05",
            end="2008-04-13 11:00:00-05",
        )

    def test_trip_creation(self):
        self.assertEquals(Trip.objects.get(title="TITLE").pk, 1),
        self.assertEquals(Trip.objects.get(origin="800 Blackwell St. Durham, NC").pk, 1),
        self.assertEquals(Trip.objects.get(destination="New York, NY").pk, 1),
        self.assertEquals(Trip.objects.get(start="2008-04-10 11:47:58-05").pk, 1),
        self.assertEquals(Trip.objects.get(end="2008-04-13 11:00:00-05").pk, 1),

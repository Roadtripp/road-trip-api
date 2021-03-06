from django.test import TestCase
import unittest
from django.test import Client
from .city_selector import *
from .models import *
from .event_searches import *

# Create your tests here.
class CitySelectorTestCase(TestCase):

    def test_find_haversine(self):
        self.assertEqual(find_haversine(32.00,-112.00,34.00,-110.00), 180.39869644898968)
        self.assertEqual(find_haversine(43.00,-89.00,25.00,-110.00), 1721.0814638308734)

    def test_find_cities(self):
        self.assertGreaterEqual(len(find_cities("Raleigh", "Boston")), 2)
        self.assertIn(('New York', 'NY'), find_cities("Raleigh", "Boston"))

    def test_get_waypoints(self):
        test = GoogleMapsDirections("Raleigh", "Boston")
        self.assertEqual(len(test.get_waypoints()), 3)
        self.assertGreaterEqual(len(test.get_waypoints()["waypoints"]), 2)

    def test_format_waypoints(self):
        test = GoogleMapsDirections("Raleigh", "Boston")
        self.assertGreaterEqual(len(test.format_waypoints()), 3)


class EventSearchesTestCase(TestCase):
    def setUp(self):
        test_trip = Trip.objects.create(
        pk=1,
        origin="Raleigh, NC",
        destination="San Diego, CA",
        origin_date="2015-11-15",
        destination_date="2015-11-20",
        title="Test Trip"
        )
        interest = Interest.objects.create(
        trip=test_trip,
        category="food",
        sub_category="chinese"
        )

    def test_get_interest_list(self):
        self.assertEqual(len(get_interest_list("food",1)), 1)
        self.assertIn("chinese", get_interest_list("food",1))

    def test_search_events(self):
        self.assertGreaterEqual(len(search_events(1)), 1)


# Create your tests here.
class TripTestCase(TestCase):
    def setUp(self):
        test_trip = Trip.objects.create(
            pk=1,
            title="TITLE",
            origin="334 Blackwell St. Durham, NC",
            origin_date="2008-04-10",
            origin_time="11:47:58-05",
            origin_lat=35.9912812,
            origin_lon=-78.9069908,
            destination="New York, NY",
            destination_lat=40.7127,
            destination_lon=-74.0059,
            destination_date="2008-04-13",
            destination_time="11:00:00-05",
        )
        #test_trip2 = Trip.objects.create(
        #     pk=2,
        #     title="TITLE",
        #     origin="334 Blackwell St. Durham, NC",
        #     origin_date="04/15/2008",
        #     origin_time="11:47:58-05",
        #     origin_lat=35.9912812,
        #     origin_lon=-78.9069908,
        #     destination="New York, NY",
        #     destination_lat=40.7127,
        #     destination_lon=-74.0059,
        #     destination_date="05/01/2008",
        #     destination_time="11:00:00-05",
        # )

    def test_trip_creation(self):
        self.assertEquals(Trip.objects.get(title="TITLE").pk, 1),
        self.assertEquals(Trip.objects.get(origin="334 Blackwell St. Durham, NC").pk, 1),
        self.assertEquals(Trip.objects.get(destination="New York, NY").pk, 1),
        self.assertEquals(Trip.objects.get(origin_date="2008-04-10").pk, 1),
        self.assertEquals(Trip.objects.get(origin_time="11:47:58-05").pk, 1),
        self.assertEquals(Trip.objects.get(destination_date="2008-04-13").pk, 1),
        self.assertEquals(Trip.objects.get(destination_time="11:00:00-05").pk, 1),
        self.assertNotEquals(Trip.objects.get(destination_time="11:00:00-05").pk, 2),

    # def test_alt_date_format(self):
    #     self.assertEquals(Trip.objects.get(origin_date="04/15/2008").pk, 2),
    #     self.assertEquals(Trip.objects.get(destination_date="05/01/2008").pk, 2),
    #     self.assertNotEquals(Trip.objects.get(destination_date="05/01/2008").pk, 1),


class CityTestCase(TestCase):
    def setUp(self):
        test_city = City.objects.create(
            pk=1,
            city_name="Washington, DC",
            lat=38.9047,
            lon=-77.0164,
            trip=Trip.objects.create(
                pk=1,
                title="TITLE",
                origin="334 Blackwell St. Durham, NC",
                origin_date="2008-04-10",
                origin_time="11:47:58-05",
                origin_lat=35.9912812,
                origin_lon=-78.9069908,
                destination="New York, NY",
                destination_lat=40.7127,
                destination_lon=-74.0059,
                destination_date="2008-04-13",
                destination_time="11:00:00-05",
            )
        )

    def test_city_creation(self):
        self.assertEquals(City.objects.get(city_name="Washington, DC").pk, 1),
        self.assertEquals(City.objects.get(lat=38.9047).pk, 1),
        self.assertEquals(City.objects.get(lon=-77.0164).pk, 1),
        self.assertEquals(City.objects.get(trip=Trip.objects.get(pk=1)).pk, 1),
        self.assertNotEquals(City.objects.get(lon=-77.0164).pk, 2),


# TODO: re-attempt testing via Client()
# class SuggestionTestCase(TestCase):
#     def setUp(self):
#         c = Client()
#         head_trip_post = {'title': 'TITLE',
#                           'origin': '334 Blackwell Street B017, Durham, NC',
#                           'origin_date': '08/25/2004', 'origin_time': '12:00 PM',
#                           'destination': 'New York, NY',
#                           'destination_date': '08/28/2004',
#                           'destination_time': '12:00 PM'}
#         url_trip_post = '/api/trip/'
#         self.res_trip_post = c.post(url_trip_post, head_trip_post)
#         self.j_trip_post = self.res_trip_post.content
#
#         url_trip_suggestions = url_trip_post + self.j_trip_post['id'] + '/suggestions/'
#         self.suggestions = c.get(url_trip_suggestions)
#
#     def test_trip_creation(self):
#         self.assertEquals(self.res_trip_post.status_code, 201)
#         self.assertIn({
#                 'location': "Washington, District of Columbia",
#                 'lat': 38.9047,
#                 'lon': -77.0164,
#                 'stopover': False
#                 }, self.suggestions['waypoints'])

from django.test import TestCase
import unittest
from .city_selector import *

# Create your tests here.
class CitySelectorTestCase(TestCase):

    def test_find_dist(self):
        self.assertEqual(find_dist(32.00,-112.00,34.00,-110.00), 180.39869644898968)
        self.assertEqual(find_dist(43.00,-89.00,25.00,-110.00), 1721.0814638308734)

    def test_find_cities(self):
        self.assertGreaterEqual(len(find_cities("Raleigh","Boston")), 2)
        self.assertIn(('New York', 'New York'), find_cities("Raleigh", "Boston"))

    def test_get_waypoints(self):
        test = GoogleMapsDirections("Raleigh", "Boston")
        self.assertEqual(len(test.get_waypoints()), 3)
        self.assertGreaterEqual(len(test.get_waypoints()["waypoints"]), 2)

    def test_format_waypoints(self):
        test= GoogleMapsDirections("Raleigh", "Boston")
        self.assertGreaterEqual(len(test.format_waypoints()), 3)

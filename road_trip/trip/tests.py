from django.test import TestCase
import unittest
from .city_selector import *

# Create your tests here.
class CitySelectorTestCase(TestCase):

    def test_find_dist(self):
        self.assertEqual(find_dist(32.00,-112.00,34.00,-110.00), 180.39869644898968)
        self.assertEqual(find_dist(43.00,-89.00,25.00,-110.00), 1721.0814638308734)

    

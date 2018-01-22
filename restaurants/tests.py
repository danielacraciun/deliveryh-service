import datetime

from django.forms import model_to_dict
from django.test import TestCase
from django_dynamic_fixture import G

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class TestRestaurantSerializer(TestCase):

    def test_serializer_with_empty_data(self):
        serializer = RestaurantSerializer(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        opening_time, closing_time = datetime.time(hour=6), datetime.time(hour=14)
        restaurant_with_schedule = G(Restaurant, opens_at=opening_time, closes_at=closing_time)

        serializer = RestaurantSerializer(data=model_to_dict(restaurant_with_schedule))
        self.assertTrue(serializer.is_valid())

    def test_serializer_validates_wrong_schedule_times(self):
        opening_time, closing_time = datetime.time(hour=11), datetime.time(hour=8)
        restaurant_with_schedule = G(Restaurant, opens_at=opening_time, closes_at=closing_time)

        serializer = RestaurantSerializer(data=model_to_dict(restaurant_with_schedule))
        self.assertFalse(serializer.is_valid())
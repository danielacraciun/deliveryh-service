import datetime

from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework import status
from rest_framework.test import APIClient

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class TestRestaurantSerializer(TestCase):

    def test_serializer_with_empty_data(self):
        serializer = RestaurantSerializer(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        open, close = datetime.time(hour=6), datetime.time(hour=14)
        restaurant = G(Restaurant, opens_at=open, closes_at=close)

        serializer = RestaurantSerializer(
            data=model_to_dict(restaurant)
        )
        self.assertTrue(serializer.is_valid())

    def test_serializer_validates_wrong_schedule_times(self):
        open, close = datetime.time(hour=11), datetime.time(hour=8)
        restaurant = G(Restaurant, opens_at=open, closes_at=close)

        serializer = RestaurantSerializer(
            data=model_to_dict(restaurant)
        )
        self.assertFalse(serializer.is_valid())


class TestRestaurantViewTestCase(TestCase):

    def setUp(self):
        open, close = datetime.time(hour=6), datetime.time(hour=14)
        self.restaurant = G(Restaurant, opens_at=open, closes_at=close)
        self.base_url = '/api/restaurants/'
        self.client = APIClient()

    def get_object_url(self, object_id):
        return self.base_url + '{}/'.format(object_id)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.base_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        valid_restaurant_data = {
            'name': 'MyRestaurant',
            'opens_at': '8:30',
            'closes_at': '11:30',
        }
        response = self.client.post(
            self.base_url, valid_restaurant_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request_returns_a_given_restaurant(self):
        response = self.client.get(self.get_object_url(self.restaurant.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['opens_at'], '06:00')
        self.assertEqual(response.json()['closes_at'], '14:00')

    def test_put_request_updates_a_restaurant(self):
        open, close  = datetime.time(hour=8), datetime.time(hour=22)
        new_restaurant = G(Restaurant, opens_at=open, closes_at=close)

        payload = model_to_dict(new_restaurant)
        response = self.client.put(
            self.get_object_url(self.restaurant.id), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['opens_at'], '08:00')
        self.assertEqual(response.json()['closes_at'], '22:00')

    def test_patch_request_partially_updates_a_restaurant(self):
        response = self.client.patch(
            self.get_object_url(self.restaurant.id), {'name': 'MyRestaurant'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'MyRestaurant')

    def test_patch_fail_validation(self):
        response = self.client.patch(
            self.get_object_url(self.restaurant.id), {'closes_at': '04:00'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'],
            ['Restaurant cannot have a closing time before an opening time']
        )

    def test_delete_request_removes_a_given_restaurant(self):
        response = self.client.delete(self.get_object_url(self.restaurant.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_request_on_missing_id_return_not_found(self):
        response = self.client.delete(self.get_object_url(-1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
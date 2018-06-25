import os

from django.conf import settings
from django.urls import reverse
from rest_framework import status

from location.models import City
from location.tests.tests import CommonTestCase


class BaseLocationCityTest(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = [
            os.path.join(settings.FIXTURES_DIR, 'location-city.json')
        ]
        super().setUpClass()

    def _create(self):
        url = reverse('location:city-list')
        print(url)
        data = {
            'name': 'test city'
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, res.json())

    def _update(self):
        city = City.objects.order_by('?').first()
        url = reverse('location:city-detail', kwargs={'pk': city.pk})
        data = {
            'name': 'updated city'
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, res.json())

    def _list(self):
        url = reverse('location:city-list')

        cnt = City.objects.all().count()

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.json())
        ret = res.json()
        self.assertEqual(cnt, len(ret))

    def _retrieve(self):
        city = City.objects.order_by('?').first()
        url = reverse('location:city-detail', kwargs={'pk': city.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.json())
        ret = res.json()
        self.assertEqual({
            'pk': city.pk,
            'name': city.name,
            'region': {
                'pk': city.region.pk,
                'name': city.region.name,
            }
        }, ret)

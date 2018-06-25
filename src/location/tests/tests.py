import uuid
from rest_framework.test import APITestCase

from accounts.models import User


class CommonTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.user = self.create_user(email='test-user@localhost', username='test-user')

    def create_user(self, model=User, **kwargs):
        _str = uuid.uuid4().hex[:4]
        data = {
            'username': 'test-{}'.format(_str),
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test-{}@localhost'.format(_str),
        }

        data.update(kwargs)
        return model.objects.create(**data)

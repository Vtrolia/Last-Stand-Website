from django.test import TestCase, Client
from django.contrib.auth.models import User
from helpers import generate_new_cert
from .models import SSL, Cloud
import datetime as dt

# Create your tests here.
class CreateCert(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        user = self.client.login()

        test_auth = generate_new_cert("test", "test", "testCloud")
        ssl = SSL.objects.create(privkey=test_auth[1], cacert=test_auth[0], date_created=dt.datetime.now(),
                           date_expires=dt.datetime.now() + dt.timedelta(days=1), created_by=self.user, owned_by=self.user)
        Cloud.objects.create(id="test", ip_address="1.1.1.1", ssl_cert=ssl, owner=self.user)

    def test_1(self):
        generate_new_cert("gamers", "rise", "up")

    def test_2(self):
        c = Client()
        response = c.post("/api/submit-cloud/", {"name": "test2", "ip": "1.2.2.2"})

        assert response.status_code < 400 and len(response.content) > 0


class GetterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        user = self.client.login(self.user)

        test_auth = generate_new_cert("test", "test", "testCloud")
        ssl = SSL.objects.create(privkey=test_auth[1], cacert=test_auth[0], date_created=dt.datetime.now(),
                                 date_expires=dt.datetime.now() + relativedelta(days=1), created_by=user, owned_by=user)
        Cloud.objects.create(id="test", ip_address="1.1.1.1", ssl_cert=SSL.ssl, owner=user)





from django.test import TestCase, Client
from django.contrib.auth.models import User
from helpers import generate_new_cert
from .models import SSL, Cloud
import datetime as dt
import re

# Create your tests here.
class CreateCert(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        self.client.login()

        test_auth = generate_new_cert("test", "test", "testCloud")
        ssl = SSL.objects.create(privkey=test_auth[1], cacert=test_auth[0], date_created=dt.datetime.now(),
                           date_expires=dt.datetime.now() + dt.timedelta(days=1), created_by=self.user, owned_by=self.user)
        Cloud.objects.create(id="test", ip_address="1.1.1.1", ssl_cert=ssl, owner=self.user)

    # make sure a private key and a certificate are returned by generate_new_cert
    def test_1(self):
        assert len(generate_new_cert("gamers", "rise", "up")) == 2

    # make sure that the returned dumps are equal to the file
    def test_2(self):
        auth = generate_new_cert("testies", "test", "testit")
        cert = open("./static/certs/testies-testit-cert.pem")
        key = open("./static/certs/testies-testit-pri.pem")

        assert cert.read() == auth[0] and key.read() == auth[1]
        cert.close()
        key.close()

    # make sure we get a correct response with a fresh key and cert when creating a new cloud, and return them as text
    # so that it can be sent to the user in a file
    def test_3(self):
        c = Client()
        c.force_login(user=self.user)
        response = c.post("/api/submit-cloud/", {"name": "test2", "ip": "1.2.2.2"})
        response_text = response.content.decode('utf-8').split("-----END CERTIFICATE-----")
        response_text[0] += "-----END CERTIFICATE-----"
        assert response.status_code < 400 and len(response_text) == 2

    # make sure that not only will renewing a cert return a cert, but also that it is new and not the same as the old one
    def test_4(self):
        c = Client()
        with open("./static/certs/test_user-test-cert.pem", "rb") as f:
            old_cert = f.read().decode('utf-8')
        c.force_login(user=self.user)
        response = c.post("/api/renew-certificate/test?user=test_user&password=password")
        assert response.status_code < 400 and old_cert != response.content.decode('utf-8')




class GetterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        self.client.login(self.user)

        test_auth = generate_new_cert("test", "test", "testCloud")
        ssl = SSL.objects.create(privkey=test_auth[1], cacert=test_auth[0], date_created=dt.datetime.now(),
                                 date_expires=dt.datetime.now() + dt.timedelta(days=1), created_by=self.user, owned_by=self.user)
        Cloud.objects.create(id="test", ip_address="1.1.1.1", ssl_cert=ssl, owner=self.user)





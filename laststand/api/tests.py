from django.test import TestCase
from helpers import generate_new_cert

# Create your tests here.
class CreateCert(TestCase):
    print(generate_new_cert("Vinny", 'ShitBag1', "Gay Little Servger"))
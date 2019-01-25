#helper functions to be used in each app to simplify many of the basic functions of the website

import hashlib as h
from OpenSSL import crypto as c
import os

from django.shortcuts import render
from django.contrib.auth import authenticate

# not a view, this function is a helper so that the user can constantly be assured that they are still logged in.
# it displays a greeting to the user with their first name, or their username if that was not provided
def return_as_wanted(request, template, message=None):
    if request.user.is_authenticated:
        if request.user.get_short_name():
            try:
                if len(request.user.get_short_name()) > 14:
                    name = request.user.get_short_name()[:11] + "..."
                else:
                    name = request.user.get_short_name()
            except:
                pass
            return render(request, template, context={"name": "Welcome Back, " + str(name) + "!",
                                                      "message": message})

        if len(request.user.get_username()) > 14:
            greeting = request.user.get_username()[:11] + "..."
        else:
            greeting = request.user.get_username()
        return render(request, template, context={"name": "Welcome Back, " + str(greeting) + "!", "message": message})

    return render(request, template, context={"message": message})


# helper function to more neatly create the SHA256 hash of the password. I know Django says that they have encryption
# built into their password validation, but I was able to see the plaintext password when I looked at the user object
def sha256_hash(password):
    return h.sha256(password.encode()).hexdigest()


# for all the functions of the api, the user making the request needs to be checked if they exist. The same authemtication
# is done each time, so I moved it to this helper
def api_user_check(request):
    user, password = request.META["QUERY_STRING"].split("&")
    user = user.split("=")[1]
    password = password.split("=")[1]

    is_user = authenticate(request, username=user, password=password)
    return is_user


def generate_new_cert(ownername, ownerpass, name, key=None):
    # create a key if this is a new cloud, otherwise load what is stored if this is just a server renewing itself
    if not key:
        key = c.PKey()
        key.generate_key(c.TYPE_RSA, 1024)
        with open("./static/certs/" + name + ".pem", "wb") as pk:
            pk.write(c.dump_privatekey(c.FILETYPE_PEM, key, passphrase=ownername + ownerpass))
    else:
        key = c.load_privatekey(c.FILETYPE_PEM, "./static/certs/" + name + ".pem", passphrase=ownername + ownerpass)

    # get laststand's key
    laststand_key =c.load_privatekey(c.FILETYPE_PEM, "privkey.pem", passphrase=os.environ.get("LASTSTAND_PRIVKEY"))

    # create the new certificate, fill it with Last Stand Cloud's information, then sign it with our private key
    new_cert = c.X509()
    new_cert.get_subject().C = "USA"
    new_cert.get_subject().ST = "Illinois"
    new_cert.get_subject().L = "Joliet"
    new_cert.get_subject().O = "Last Stand Cloud Software"
    new_cert.get_subject().CN = "Last Stand Cloud"
    new_cert.set_issuer(new_cert.get_subject())
    new_cert.set_pubkey(key)
    new_cert.sign(laststand_key, "sha256")

    # dump the new cert so it can be kept until it expires, sort of like the gold in Fort Knox backing up the dollar
    with open("./static/certs/" + name + ".cacert", "wb") as cert:
        cert.write(c.dump_certificate(c.FILETYPE_PEM, new_cert))

    return new_cert, key


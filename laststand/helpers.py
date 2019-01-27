#helper functions to be used in each app to simplify many of the basic functions of the website

import hashlib as h
from OpenSSL import crypto as c
import os, random, time

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

# the second usage of my old password generator program, is being revived as the function that created the ids of
# the clouds. Good ol' TroliAlgorithm. Presented in its original, horribly designed form
def TroliAlgorithm(word1, word2):
    """Takes in two words, word 1 and word 2. If the words provided are
       not empty, it puts them through the algorithm and returns a pseudo-
       random string of characters that are dependant on the words entered.
       I made it so that even the same inputs will result in a different
       output every time, making the generated passwords harder to predict"""

    # initialize the list of eventual characters and repeatedly makes sure
    # that none of the words are empty
    password = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    ascii_let = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                 'W', 'X', 'Y', 'Z']

    # this code runs of both words are even or both are odd in length
    if ((len(word2) + len(word1)) % 2) == 0:
        try:
            password[0] = int((len(word1) + len(word2)) / len(word1))

        except ZeroDivisionError:
            return "one of your words is empty!"
        try:
            if (len(word1) < 1) and (len(word2) < 1):
                password[1] = (word1[password[0]]) + (word2[password[0]])
            else:
                password[1] = word1[0] + word2[0]
        except IndexError:
            return "one of your words is empty!"

        password[2] = abs(len(word1) - len(word2))
        temp = password[2]
        while temp >= len(word1):
            temp -= len(word1)
        password[3] = word1[temp]
        password[4] = int(round(random.randrange(1, int(time.time())), 1) / 1000)
        password[5] = random.choice(ascii_let)
        if len(word2) > len(word1):
            password[6] = random.randrange(len(word1), (len(word2) + 1))
        else:
            password[6] = random.randrange(len(word2), (len(word1) + 1))
        password[7] = chr(password[6] + 95)
        password[8] = (ord(password[5]) * password[6])

        # takes letters from both words and adds them at the end
        # utilization of the dictionary.txt values make this a great addition
        password[9] = ""
        if len(word1) > len(word2):
            max0 = len(word2)
        else:
            max0 = len(word1)
        for j in range(max0 % 4):
            try:
                password[9] += word1[j] + word2[j]
            except IndexError:
                return "one of your words is empty!"

    # this code runs if one word is odd and the other is even; it switches
    # up the layout of the passwords to reduce repitition
    else:
        password[0] = random.choice(ascii_let)
        try:
            password[1] = int((len(word1) + len(word2)) / len(word1))
        except ZeroDivisionError:
            return "one of your words is empty!"

        password[2] = ""
        if len(word1) > len(word2):
            max1 = len(word2) // 2
        else:
            max1 = len(word1) // 2
        for j in range(max1):
            try:
                password[2] += word1[j] + word2[j]
            except IndexError:
                return "one of your words is empty!"
        if len(word2) > len(word1):
            password[6] = random.randrange(len(word1), (len(word2) + 1))
        else:
            password[6] = random.randrange(len(word2), (len(word1) + 1))
        password[4] = chr(password[1] + 95)
        password[5] = (ord(password[4]) * password[3])
        password[6] = abs(len(word1) - len(word2))
        temp1 = password[6]
        while temp1 >= len(word1):
            temp1 -= len(word1)
        password[7] = word1[temp1]
        password[8] = int(round(random.randrange(1, int(time.time())), 1) / 1000)
        try:
            if (len(word1) < 1) and (len(word2) < 1):
                password[9] = (word1[password[0]]) + (word2[password[0]])
            else:
                password[9] = word1[0] + word2[0]
        except IndexError:
            return "one of your words is empty!"

    # fixes a bug where some characters turn out as "`" then converts
    # the new password to a string that returns to the calling variable
    # or functions
    for i in range(10):
        if password[i] == '`':
            password[i] = random.choice(ascii_let)
        password[i] = str(password[i])

    pasw = ''.join(password)
    return pasw
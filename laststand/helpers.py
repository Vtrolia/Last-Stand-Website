#helper functions to be used in each app to simplify many of the basic functions of the website

import hashlib as h
from django.shortcuts import render

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
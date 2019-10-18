"""
WSGI config for lsv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsv.settings')
path='usr/local/www/Last-Stand-Website/verify/lsv'
if path not in sys.path:
    sys.path.append(path)
application = get_wsgi_application()

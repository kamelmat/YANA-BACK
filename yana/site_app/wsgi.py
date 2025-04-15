"""
WSGI config for site_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Use test settings when running tests
if 'test' in sys.argv:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_app.settings.production')

application = get_wsgi_application()

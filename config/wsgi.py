# flake8: noqa: E402
import os

import eventlet
from django.core.wsgi import get_wsgi_application

eventlet.monkey_patch()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

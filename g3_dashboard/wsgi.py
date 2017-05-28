"""
WSGI config for g3_dashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

#from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ubuntu/3g_admin/3g-dashboard')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "g3_dashboard.settings")
sys.path.append("/home/ubuntu/3g_admin/env/lib/python3.5/site-packages")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "g3_dashboard.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

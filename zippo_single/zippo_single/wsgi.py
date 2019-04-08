"""
WSGI config for zippo_single project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
from os.path import join,dirname,abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
from django.core.wsgi import get_wsgi_application
sys.path.insert(0,PROJECT_DIR) # 5
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zippo_single.settings")

application = get_wsgi_application()

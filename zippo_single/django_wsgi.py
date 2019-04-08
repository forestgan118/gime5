#!/usr/bin/env python
# coding: utf-8

import os
import sys
print(sys.path)
import django.core
import django.core.handlers
import importlib
# 将系统的编码设置为UTF8
importlib.reload(sys)
#sys.setdefaultencoding('utf8')
sys.path.append('/home/env/zippo/zippo_single')
sys.path.append('/home/env/zippo/zippo_single/zippo_single')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zippo_single.settings")

#from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application
#application = WSGIHandler()
application = get_wsgi_application()
"""
WSGI config for venuemap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from project_setup import main as project_setup_main

if __name__ == '__main__':
    project_setup_main()
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoursettings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venuemap.settings')

application = get_wsgi_application()

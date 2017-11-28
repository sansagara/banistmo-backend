#!/bin/bash
source development_settings.sh
python3 manage.py migrate

#If first run, then uncomment next line:
# python3 manage.py createsuperuser

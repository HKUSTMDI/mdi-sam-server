#!/bin/bash

# Execute the gunicorn command
#gunicorn --preload --bind :9091 --workers 1 --threads 8 --timeout 0 _wsgi:app
nohup python3 _wsgi.py --port 9091 >> run.log &

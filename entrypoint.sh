#!/bin/sh
# entrypoint.sh
gunicorn --bind :3000 --workers 2 app:main &
python3 app.py

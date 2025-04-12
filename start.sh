#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT \
         --worker-class gevent \  # <-- THIS IS CRITICAL
         --workers 3 \
         --timeout 600 \
         --keep-alive 120 \
         --access-logfile - \
         --error-logfile - \
         backend:app
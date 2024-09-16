#!/usr/bin/env bash


cd /app
source .env
workers=4
gunicorn server.main:app --workers $workers -k uvicorn.workers.UvicornWorker --timeout 1800  --worker-class uvicorn.workers.UvicornWorker  --access-logfile - --error-logfile - --log-level debug --bind 0.0.0.0:8000
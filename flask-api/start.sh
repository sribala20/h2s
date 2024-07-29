#!/bin/bash
cd /flask-api
exec gunicorn -b 0.0.0.0:5000 server:app
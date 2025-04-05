#!/bin/bash

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Start Flask on all interfaces, port 8081
flask run --host=0.0.0.0 --port=8081

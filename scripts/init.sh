#!/bin/bash
./expect.sh
python3 -m venv /app/venv
. /app/venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 8080 --host 0.0.0.0 &
echo "Flask app and React app are now running in the background."
# Keep the script running
tail -f /dev/null
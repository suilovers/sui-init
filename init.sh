#!/bin/bash
# rust setup

rustup default stable

# for initial process
chmod +x expect.sh
./expect.sh

current_dir=$(pwd)
# Run Flask app in the background
cd $current_dir/backend
python3 -m venv /app/venv
. /app/venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 8080 --host 0.0.0.0 &

# Optional: Add a delay to ensure that the Flask app starts before the React app
sleep 5

# Run React app in the background
cd $current_dir/ui
npm start &

# Optional: Print a message indicating that both apps are running
echo "Flask app and React app are now running in the background."

# Keep the script running
tail -f /dev/null
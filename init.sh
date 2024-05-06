#!/bin/bash

# for initial process
spawn sui client
expect "Config file ["/root/.sui/sui_config/client.yaml"] doesn't exist, do you want to connect to a Sui Full node server [y/N]?"
send "n\r"
expect "Sui Full node server URL (Defaults to Sui Testnet if not specified) :"
send "\r"
expect "Select key scheme to generate keypair (0 for ed25519, 1 for secp256k1, 2: for secp256r1):"
send "0\r"

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
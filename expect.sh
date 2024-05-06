#!/usr/bin/expect -f

spawn sui client
expect "Config file \[\"/root/.sui/sui_config/client.yaml\"\] doesn't exist, do you want to connect to a Sui Full node server \[y/N\]?"
send "y\r"
expect "Sui Full node server URL (Defaults to Sui Testnet if not specified) :"
send "\r"
expect "Select key scheme to generate keypair (0 for ed25519, 1 for secp256k1, 2: for secp256r1):"
send "0\r"
expect eof
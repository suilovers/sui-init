#!/bin/bash

# check if /root/.sui exists
if [ ! -d "/root/.sui" ]; then
    # create /root/.sui
    sui genesis
fi

# start sui local network
echo "Starting Sui Localnet ..."
sui start &

while ! curl -s http://127.0.0.1:9000 > /dev/null; do echo Waiting for Sui Localnet ...; sleep 3; done
echo "Sui Localnet is ready!"

echo "Starting Sui Faucet ..."
sui-faucet --num-coins 10  --write-ahead-log /tmp/sui-facucel.wal --host-ip 0.0.0.0 --port 9123 &

while ! curl -s http://127.0.0.1:9123 > /dev/null; do echo Waiting for Sui Faucet ...; sleep 3; done
echo "Sui Faucet is ready!"

wait
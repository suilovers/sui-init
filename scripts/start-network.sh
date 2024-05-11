#!/bin/bash

# start the network
sui-test-validator --config-dir /root/.sui/sui_config --indexer-rpc-port 9124 --fullnode-rpc-port 7000

tail -f /dev/null
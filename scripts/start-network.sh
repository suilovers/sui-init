#!/bin/bash

# start the network
sui-test-validator \
    --config-dir /root/.sui/sui_config \
    --indexer-rpc-port 9124 \
    --fullnode-rpc-port 7000 \
    --graphql-host 127.0.0.1 \
    --graphql-port 8000 \
    --with-indexer \ 

tail -f /dev/null
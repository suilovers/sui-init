#!/bin/bash

# Array of commands
commands=(
    "active-address"
    "active-env"
    "addresses"
    "balance"
    "call"
    "chain-identifier"
    "dynamic-field"
    "envs"
    "execute-signed-tx"
    "execute-combined-signed-tx"
    "faucet"
    "gas"
    "merge-coin"
    "new-address"
    "new-env"
    "object"
    "objects"
    "pay"
    "pay-all-sui"
    "pay-sui"
    "ptb"
    "publish"
    "split-coin"
    "switch"
    "tx-block"
    "transfer"
    "transfer-sui"
    "upgrade"
    "verify-bytecode-meter"
    "verify-source"
    "profile-transaction"
    "replay-transaction"
    "replay-batch"
    "replay-checkpoint"
)

# Loop through each command and call with --help
for cmd in "${commands[@]}"; do
    echo "Calling 'sui client $cmd --help':"
    sui client "$cmd" --help
    echo ""
done

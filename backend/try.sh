#!/bin/bash

# Array of commands
commands=(
    "update-alias"
    "convert"
    "decode-or-verify-tx"
    "decode-multi-sig"
    "generate"
    "import"
    "export"
    "list"
    "load-keypair"
    "multi-sig-address"
    "multi-sig-combine-partial-sig"
    "multi-sig-combine-partial-sig-legacy"
    "show"
    "sign"
    "sign-kms"
    "unpack"
    "zk-login-sign-and-execute-tx"
    "zk-login-enter-token"
    "zk-login-sig-verify"
    "zk-login-insecure-sign-personal-message"
)

# Loop through each command and call with --help
for cmd in "${commands[@]}"; do
    echo "Calling 'sui keytool $cmd --help':"
    sui keytool "$cmd" --help
    echo ""
done

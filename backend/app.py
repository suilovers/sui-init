import re
from flask import Blueprint, Flask, request, jsonify
import subprocess
import json

from pydantic import ValidationError
from dto import (
    StartDTO,
    ClientBalanceDTO,
    KeytoolConvertDTO,
    ClientCallDTO,
    ClientPtbDTO,
    ClientNewEnvDTO,
    ClientPaySuiDTO,
    ClientExecuteCombinedSignedTxDTO,
    ClientPayDTO,
    ClientExecuteSignedTxDTO,
    ClientDynamicFieldDTO,
    ClientPayAllSuiDTO,
)
from utils import sui_command, cat_command

app = Flask(__name__)
api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/start", methods=["POST"])
def start():
    """
    Starts the application with the provided configuration.

    Returns:
        The response from the `sui_command` function.
    """
    data = StartDTO(**request.json)
    command = ["start"]
    if data.network_config:
        command.extend(["--network.config", data.network_config])
    if data.no_full_node:
        command.append("--no-full-node")
    response = sui_command(command, isJson=False)
    return response


### CLIENT ENDPOINTS ###
@api_blueprint.route("/client/active-address", methods=["GET"])
def client_active_address():
    """
    Retrieves the active address of the client.

    Returns:
        dict: A dictionary containing the active address.
            Example: {"active_address": "123 Main St"}
    """
    response = sui_command(["client", "active-address"])
    return {"active_address": response}


@api_blueprint.route("/client/active-env", methods=["GET"])
def client_active_env():
    response = sui_command(["client", "active-env"])
    return {"active_env": response}


@api_blueprint.route("/client/addresses", methods=["GET"])
def client_addresses():
    response = sui_command(["client", "addresses"])
    return response


@api_blueprint.route("/client/balance", methods=["POST"])
def client_balance():
    data = ClientBalanceDTO(**request.json)
    command = ["client", "balance", data.address]
    if data.coin_type:
        command.extend(["--coin-type", data.coin_type])
    if data.with_coins:
        command.append("--with-coins")
    response = sui_command(command)
    return response


@api_blueprint.route("/client/call", methods=["POST"])
def client_call():
    data = ClientCallDTO(**request.json)
    command = [
        "client",
        "call",
        "--package",
        data.package,
        "--module",
        data.module,
        "--function",
        data.function,
        "--gas-budget",
        data.gas_budget,
    ]
    if data.type_args:
        for arg in data.type_args:
            command.extend(["--type-args", arg])
    if data.args:
        for arg in data.args:
            command.extend(["--args", arg])
    if data.gas:
        command.extend(["--gas", data.gas])
    if data.dry_run:
        command.append("--dry-run")
    if data.serialize_unsigned_transaction:
        command.append("--serialize-unsigned-transaction")
    if data.serialize_signed_transaction:
        command.append("--serialize-signed-transaction")
    response = sui_command(command)
    return response


@api_blueprint.route("/client/chain-identifier", methods=["GET"])
def client_chain_identifier():
    command = ["client", "chain-identifier"]
    response = sui_command(command)
    return response


@api_blueprint.route("/client/dynamic-field", methods=["POST"])
def client_dynamic_field():
    data = ClientDynamicFieldDTO(**request.json)
    command = ["client", "dynamic-field", data.object_id]
    if data.cursor:
        command.extend(["--cursor", data.cursor])
    if data.limit:
        command.extend(["--limit", str(data.limit)])
    response = sui_command(command)
    return response


@api_blueprint.route("/client/execute-signed-tx", methods=["POST"])
def client_execute_signed_tx():
    try:
        data = ClientExecuteSignedTxDTO(**request.json)
        command = ["client", "execute-signed-tx", "--tx-bytes", data.tx_bytes]
        if data.signatures:
            command.extend(["--signatures"] + data.signatures)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/execute-combined-signed-tx", methods=["POST"])
def client_execute_combined_signed_tx():
    try:
        data = ClientExecuteCombinedSignedTxDTO(**request.json)
        command = [
            "client",
            "execute-combined-signed-tx",
            "--signed-tx-bytes",
            data.signed_tx_bytes,
        ]
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/new-env", methods=["POST"])
def client_new_env():
    try:
        data = ClientNewEnvDTO(**request.json)
        command = ["client", "new-env", "--alias", data.alias, "--rpc", data.rpc]
        if data.ws:
            command.extend(["--ws", data.ws])
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/pay", methods=["POST"])
def client_pay():
    try:
        data = ClientPayDTO(**request.json)
        command = ["client", "pay", "--gas-budget", data.gas_budget]
        command.extend(["--input-coins"] + data.input_coins)
        command.extend(["--recipients"] + data.recipients)
        command.extend(["--amounts"] + data.amounts)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/pay-all-sui", methods=["POST"])
def client_pay_all_sui():
    try:
        data = ClientPayAllSuiDTO(**request.json)
        command = [
            "client",
            "pay-all-sui",
            "--recipient",
            data.recipient,
            "--gas-budget",
            data.gas_budget,
        ]
        command.extend(["--input-coins"] + data.input_coins)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/pay-sui", methods=["POST"])
def client_pay_sui():
    try:
        data = ClientPaySuiDTO(**request.json)
        command = ["client", "pay-sui", "--gas-budget", data.gas_budget]
        command.extend(["--input-coins"] + data.input_coins)
        command.extend(["--recipients"] + data.recipients)
        command.extend(["--amounts"] + data.amounts)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/ptb", methods=["POST"])
def client_ptb():
    try:
        data = ClientPtbDTO(**request.json)
        command = ["client", "ptb"]
        if data.assign:
            for name, value in data.assign.items():
                command.extend(["--assign", name, value])
        if data.gas_coin:
            command.extend(["--gas-coin", data.gas_coin])
        if data.gas_budget:
            command.extend(["--gas-budget", data.gas_budget])
        # Add similar checks for other options...
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/private", methods=["GET"])
def client_private():
    response = cat_command(
        "~/.sui/sui_config/sui.keystore", isJson=True, name="private_key"
    )
    return {"private_keys": response}


#### KEYTOOL ENDPOINTS ####
@api_blueprint.route("/keytools/convert", methods=["POST"])
def keytool_convert():
    data = KeytoolConvertDTO(**request.json)
    command = ["keytool", "convert", data.value]
    response = sui_command(command)
    return response


app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)

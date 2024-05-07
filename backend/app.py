import json
import subprocess
from flask import Blueprint, Flask, request, jsonify

from flask_cors import CORS, cross_origin
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
    ClientFaucetDTO,
    ClientNewAddressDTO,
    ClientMergeCoinDTO,
    ClientGasDTO,
    ClientObjectsDTO,
    ClientObjectDTO,
    ClientPublishDTO,
    ClientSplitCoinDTO,
    ClientSwitchDTO,
    ClientProfileTransactionDTO,
    ClientReplayTransactionDTO,
    ClientReplayBatchDTO,
    ClientReplayCheckpointDTO,
    ClientTransferDTO,
    ClientTransferSuiDTO,
    ClientUpgradeDTO,
    ClientVerifyBytecodeMeterDTO,
    ClientTxBlockDTO,
    ClientVerifySourceDTO,
    KeytoolDecodeMultiSigDTO,
    KeytoolDecodeOrVerifyTxDTO,
    KeytoolExportDTO,
    KeytoolGenerateDTO,
    KeytoolImportDTO,
    KeytoolLoadKeypairDTO,
    KeytoolUpdateAliasDTO,
    TypeDTO,
)
from utils import sui_command, cat_command

app = Flask(__name__)
cors = CORS(app, resource={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
client_blueprint = Blueprint("client", __name__)
keytool_blueprint = Blueprint("keytool", __name__)
start_blueprint = Blueprint("start", __name__)
info_blueprint = Blueprint("info", __name__)


# @start_blueprint.route("/", methods=["POST"])
# def start():
#     """
#     Starts the application with the provided configuration.

#     Returns:
#         The response from the `sui_command` function.
#     """
#     data = StartDTO(**request.json)
#     command = ["start"]
#     if data.network_config:
#         command.extend(["--network.config", data.network_config])
#     if data.no_full_node:
#         command.append("--no-full-node")
#     response = sui_command(command, isJson=False)
#     return response


### CLIENT ENDPOINTS ###
@client_blueprint.route("/", methods=["GET"])
def client():
    command = ["sui", "client"]  # Assuming "sui" is the executable name

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(input=b"y\n\n0\n")
    print("Output:", output.decode(), "Error:", error.decode())
    main_output = "s"
    return main_output

    # if error:
    #     print("Error:", error.decode())
    #     main_output = error.decode()
    # else:
    #     # Pipe the output to echo and print the result (assuming text output)
    #     echo_process = subprocess.Popen(
    #         ["echo", "y"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
    #     )
    #     echo_output, echo_error = echo_process.communicate(input=output)
    #     if echo_error:
    #         print()
    #         print("Error in echo:", echo_error.decode())
    #         main_output = echo_error.decode()
    #     else:
    #         print()
    #         print("Combined Output:", echo_output.decode())
    #         main_output = echo_output.decode()
    #     return main_output


@client_blueprint.route("/active-address", methods=["GET"])
def client_active_address():
    """
    Retrieves the active address of the client.

    Returns:
        dict: A dictionary containing the active address.
            Example: {"active_address": "123 Main St"}
    """
    response = sui_command(["client", "active-address"])
    return {"active_address": response}


@client_blueprint.route("/active-env", methods=["GET"])
def client_active_env():
    response = sui_command(["client", "active-env"])
    return {"active_env": response}


@client_blueprint.route("/addresses", methods=["GET"])
def client_addresses():
    response = sui_command(["client", "addresses"])
    return response

@client_blueprint.route("/balance", methods=["GET"])
def current_balance():
    response = sui_command(["client", "balance"])
    return jsonify(response)

@client_blueprint.route("/balance", methods=["POST"])
def client_balance():
    data = ClientBalanceDTO(**request.json)
    command = ["client", "balance", data.address]
    if data.coin_type:
        command.extend(["--coin-type", data.coin_type])
    if data.with_coins:
        command.append("--with-coins")
    print(command)
    response = sui_command(command)
    return jsonify(response)

@client_blueprint.route("/call", methods=["POST"])
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

    if data.package:
        command.extend(["--package", data.package])
    if data.module:
        command.extend(["--module", data.module])
    if data.function:
        command.extend(["--function", data.function])
    if data.type_args:
        for arg in data.type_args:
            command.extend(["--type-args", arg])
    if data.gas_budget:
        command.extend(["--gas-budget", data.gas_budget])
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


@client_blueprint.route("/chain-identifier", methods=["GET"])
def client_chain_identifier():
    command = ["client", "chain-identifier"]
    response = sui_command(command)
    return response


@client_blueprint.route("/dynamic-field", methods=["POST"])
def client_dynamic_field():
    data = ClientDynamicFieldDTO(**request.json)
    command = ["client", "dynamic-field", data.object_id]
    if data.cursor:
        command.extend(["--cursor", data.cursor])
    if data.limit:
        command.extend(["--limit", str(data.limit)])
    response = sui_command(command)
    return response


@client_blueprint.route("/envs", methods=["GET"])
def client_envs():
    try:
        command = ["client", "envs"]
        response = sui_command(command)
        return jsonify(response)
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/execute-signed-tx", methods=["POST"])
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


@client_blueprint.route("/execute-combined-signed-tx", methods=["POST"])
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


@client_blueprint.route("/faucet", methods=["GET"])
def client_faucet():
    try:
        data = ClientFaucetDTO(**request.args)
        command = ["client", "faucet"]
        if data.address:
            command.extend(["--address", data.address])
        if data.url:
            command.extend(["--url", data.url])
        response = sui_command(command)
        print(response)
        return jsonify(response)
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/gas", methods=["GET"])
def client_gas():
    try:
        data = ClientGasDTO(**request.args)
        command = ["client", "gas"]
        if data.owner_address:
            command.append(data.owner_address)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/merge-coin", methods=["POST"])
def client_merge_coin():
    try:
        data = ClientMergeCoinDTO(**request.json)
        command = [
            "client",
            "merge-coin",
            "--primary-coin",
            data.primary_coin,
            "--coin-to-merge",
            data.coin_to_merge,
            "--gas-budget",
            data.gas_budget,
        ]
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
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/new-address", methods=["POST"])
def client_new_address():
    try:
        data = ClientNewAddressDTO(**request.json)
        command = ["client", "new-address", data.key_scheme]
        if data.alias:
            command.append(data.alias)
        if data.word_length:
            command.append(data.word_length)
        if data.derivation_path:
            command.append(data.derivation_path)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/new-env", methods=["POST"])
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


@client_blueprint.route("/object", methods=["GET"])
def client_object():
    try:
        data = ClientObjectDTO(**request.args)
        command = ["client", "object", data.object_id]
        if data.bcs:
            command.append("--bcs")
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/objects", methods=["GET"])
def client_objects():
    try:
        data = ClientObjectsDTO(**request.args)
        command = ["client", "objects"]
        if data.owner_address:
            command.append(data.owner_address)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@client_blueprint.route("/pay", methods=["POST"])
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


@client_blueprint.route("/pay-all-sui", methods=["POST"])
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


@client_blueprint.route("/pay-sui", methods=["POST"])
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


@client_blueprint.route("/ptb", methods=["POST"])
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


@client_blueprint.route("/publish", methods=["POST"])
def client_publish():
    data = ClientPublishDTO(**request.json)
    command = ["client", "publish", "--gas-budget", data.gas_budget]
    if data.package_path != ".":
        command.append(data.package_path)
    if data.dev:
        command.append("--dev")
    if data.test:
        command.append("--test")
    if data.doc:
        command.append("--doc")
    if data.install_dir:
        command.extend(["--install-dir", data.install_dir])
    if data.force:
        command.append("--force")
    if data.fetch_deps_only:
        command.append("--fetch-deps-only")
    if data.skip_fetch_latest_git_deps:
        command.append("--skip-fetch-latest-git-deps")
    if data.default_move_flavor:
        command.extend(["--default-move-flavor", data.default_move_flavor])
    if data.default_move_edition:
        command.extend(["--default-move-edition", data.default_move_edition])
    if data.dependencies_are_root:
        command.append("--dependencies-are-root")
    if data.silence_warnings:
        command.append("--silence-warnings")
    if data.warnings_are_errors:
        command.append("--warnings-are-errors")
    if data.no_lint:
        command.append("--no-lint")
    if data.lint:
        command.append("--lint")
    if data.gas:
        command.extend(["--gas", data.gas])
    if data.dry_run:
        command.append("--dry-run")
    if data.serialize_unsigned_transaction:
        command.append("--serialize-unsigned-transaction")
    if data.serialize_signed_transaction:
        command.append("--serialize-signed-transaction")
    if data.skip_dependency_verification:
        command.append("--skip-dependency-verification")
    if data.with_unpublished_dependencies:
        command.append("--with-unpublished-dependencies")
    response = sui_command(command)
    return response


@client_blueprint.route("/split-coin", methods=["POST"])
def client_split_coin():
    data = ClientSplitCoinDTO(**request.json)
    command = [
        "client",
        "split-coin",
        "--coin-id",
        data.coin_id,
        "--gas-budget",
        data.gas_budget,
    ]
    if data.amounts:
        command.extend(["--amounts"] + list(map(str, data.amounts)))
    if data.count:
        command.extend(["--count", str(data.count)])
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


@client_blueprint.route("/switch", methods=["POST"])
def client_switch():
    data = ClientSwitchDTO(**request.json)
    command = ["client", "switch"]
    if data.address:
        command.extend(["--address", data.address])
    if data.env:
        command.extend(["--env", data.env])
    response = sui_command(command)
    return response


@client_blueprint.route("/tx-block", methods=["POST"])
def client_tx_block():
    data = ClientTxBlockDTO(**request.json)
    command = ["client", "tx-block", data.digest]
    response = sui_command(command)
    return response


@client_blueprint.route("/transfer", methods=["POST"])
def client_transfer():
    data = ClientTransferDTO(**request.json)
    command = [
        "client",
        "transfer",
        "--to",
        data.to,
        "--object-id",
        data.object_id,
        "--gas-budget",
        data.gas_budget,
    ]
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


@client_blueprint.route("/transfer-sui", methods=["POST"])
def client_transfer_sui():
    data = ClientTransferSuiDTO(**request.json)
    command = [
        "client",
        "transfer-sui",
        "--to",
        data.to,
        "--sui-coin-object-id",
        data.sui_coin_object_id,
        "--gas-budget",
        data.gas_budget,
    ]
    if data.amount:
        command.extend(["--amount", data.amount])
    if data.dry_run:
        command.append("--dry-run")
    if data.serialize_unsigned_transaction:
        command.append("--serialize-unsigned-transaction")
    if data.serialize_signed_transaction:
        command.append("--serialize-signed-transaction")
    response = sui_command(command)
    return response


@client_blueprint.route("/upgrade", methods=["POST"])
def client_upgrade():
    data = ClientUpgradeDTO(**request.json)
    command = [
        "client",
        "upgrade",
        "--upgrade-capability",
        data.upgrade_capability,
        "--gas-budget",
        data.gas_budget,
    ]
    if data.package_path:
        command.append(data.package_path)
    if data.dev:
        command.append("--dev")
    if data.test:
        command.append("--test")
    if data.doc:
        command.append("--doc")
    if data.install_dir:
        command.extend(["--install-dir", data.install_dir])
    if data.force:
        command.append("--force")
    if data.fetch_deps_only:
        command.append("--fetch-deps-only")
    if data.skip_fetch_latest_git_deps:
        command.append("--skip-fetch-latest-git-deps")
    if data.default_move_flavor:
        command.extend(["--default-move-flavor", data.default_move_flavor])
    if data.default_move_edition:
        command.extend(["--default-move-edition", data.default_move_edition])
    if data.dependencies_are_root:
        command.append("--dependencies-are-root")
    if data.silence_warnings:
        command.append("--silence-warnings")
    if data.warnings_are_errors:
        command.append("--warnings-are-errors")
    if data.no_lint:
        command.append("--no-lint")
    if data.lint:
        command.append("--lint")
    if data.gas:
        command.extend(["--gas", data.gas])
    if data.dry_run:
        command.append("--dry-run")
    if data.serialize_unsigned_transaction:
        command.append("--serialize-unsigned-transaction")
    if data.serialize_signed_transaction:
        command.append("--serialize-signed-transaction")
    if data.skip_dependency_verification:
        command.append("--skip-dependency-verification")
    if data.with_unpublished_dependencies:
        command.append("--with-unpublished-dependencies")
    response = sui_command(command)
    return response


@client_blueprint.route("/verify-bytecode-meter", methods=["POST"])
def client_verify_bytecode_meter():
    data = ClientVerifyBytecodeMeterDTO(**request.json)
    command = ["client", "verify-bytecode-meter", "--package", data.package]
    if data.protocol_version:
        command.extend(["--protocol-version", data.protocol_version])
    if data.module:
        for module in data.module:
            command.extend(["--module", module])
    if data.dev:
        command.append("--dev")
    if data.test:
        command.append("--test")
    if data.doc:
        command.append("--doc")
    if data.install_dir:
        command.extend(["--install-dir", data.install_dir])
    if data.force:
        command.append("--force")
    if data.fetch_deps_only:
        command.append("--fetch-deps-only")
    if data.skip_fetch_latest_git_deps:
        command.append("--skip-fetch-latest-git-deps")
    if data.default_move_flavor:
        command.extend(["--default-move-flavor", data.default_move_flavor])
    if data.default_move_edition:
        command.extend(["--default-move-edition", data.default_move_edition])
    if data.dependencies_are_root:
        command.append("--dependencies-are-root")
    if data.silence_warnings:
        command.append("--silence-warnings")
    if data.warnings_are_errors:
        command.append("--warnings-are-errors")
    if data.no_lint:
        command.append("--no-lint")
    if data.lint:
        command.append("--lint")
    response = sui_command(command)
    return response


@client_blueprint.route("/verify-source", methods=["POST"])
def client_verify_source():
    data = ClientVerifySourceDTO(**request.json)
    command = ["client", "verify-source", data.package_path]
    if data.dev:
        command.append("--dev")
    if data.test:
        command.append("--test")
    if data.doc:
        command.append("--doc")
    if data.install_dir:
        command.extend(["--install-dir", data.install_dir])
    if data.force:
        command.append("--force")
    if data.fetch_deps_only:
        command.append("--fetch-deps-only")
    if data.skip_fetch_latest_git_deps:
        command.append("--skip-fetch-latest-git-deps")
    if data.default_move_flavor:
        command.extend(["--default-move-flavor", data.default_move_flavor])
    if data.default_move_edition:
        command.extend(["--default-move-edition", data.default_move_edition])
    if data.dependencies_are_root:
        command.append("--dependencies-are-root")
    if data.silence_warnings:
        command.append("--silence-warnings")
    if data.warnings_are_errors:
        command.append("--warnings-are-errors")
    if data.no_lint:
        command.append("--no-lint")
    if data.lint:
        command.append("--lint")
    if data.verify_deps:
        command.append("--verify-deps")
    if data.skip_source:
        command.append("--skip-source")
    if data.address_override:
        command.extend(["--address-override", data.address_override])
    response = sui_command(command)
    return response


@client_blueprint.route("/profile-transaction", methods=["POST"])
def client_profile_transaction():
    data = ClientProfileTransactionDTO(**request.json)
    command = ["client", "profile-transaction", "--tx-digest", data.tx_digest]
    if data.profile_output:
        command.extend(["--profile-output", data.profile_output])
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@client_blueprint.route("/replay-transaction", methods=["POST"])
def client_replay_transaction():
    data = ClientReplayTransactionDTO(**request.json)
    command = ["client", "replay-transaction", "--tx-digest", data.tx_digest]
    if data.gas_info:
        command.append("--gas-info")
    if data.ptb_info:
        command.append("--ptb-info")
    if data.executor_version:
        command.extend(["--executor-version", data.executor_version])
    if data.protocol_version:
        command.extend(["--protocol-version", data.protocol_version])
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@client_blueprint.route("/replay-batch", methods=["POST"])
def client_replay_batch():
    data = ClientReplayBatchDTO(**request.json)
    command = ["client", "replay-batch", "--path", data.path]
    if data.terminate_early:
        command.append("--terminate-early")
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@client_blueprint.route("/replay-checkpoint", methods=["POST"])
def client_replay_checkpoint():
    data = ClientReplayCheckpointDTO(**request.json)
    command = [
        "client",
        "replay-checkpoint",
        "--start",
        str(data.start),
        "--end",
        str(data.end),
    ]
    if data.terminate_early:
        command.append("--terminate-early")
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@client_blueprint.route("/private", methods=["GET"])
def client_private():
    response = cat_command(
        "~/.sui/sui_config/sui.keystore", isJson=True, name="private_key"
    )
    return {"private_keys": response}


#### KEYTOOL ENDPOINTS ####


@keytool_blueprint.route("/update-alias", methods=["POST"])
def update_alias():
    try:
        data = request.get_json()
        dto = KeytoolUpdateAliasDTO(**data)
    except:
        return jsonify({"error": "old_alias is required"}), 400

    # Call the 'sui keytool update-alias' command with the provided aliases
    command = ["keytool", "update-alias", dto.old_alias]
    if dto.new_alias:
        command.append(dto.new_alias)
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json()
        dto = KeytoolConvertDTO(**data)
    except:
        return jsonify({"error": "value is required"}), 400

    # Call the 'sui keytool convert' command with the provided value
    command = ["keytool", "convert", dto.value]
    output = sui_command(command)

    return {"output": output}


@keytool_blueprint.route("/decode-or-verify-tx", methods=["POST"])
def decode_or_verify_tx():
    data = request.get_json()
    dto = KeytoolDecodeOrVerifyTxDTO(**data)
    command = ["keytool", "decode-or-verify-tx", "--tx-bytes", dto.tx_bytes]
    if dto.sig:
        command.extend(["--sig", dto.sig])
    if dto.cur_epoch:
        command.extend(["--cur-epoch", str(dto.cur_epoch)])
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/decode-multi-sig", methods=["POST"])
def decode_multi_sig():
    data = request.get_json()
    dto = KeytoolDecodeMultiSigDTO(**data)
    command = ["keytool", "decode-multi-sig", "--multisig", dto.multisig]
    if dto.tx_bytes:
        command.extend(["--tx-bytes", dto.tx_bytes])
    if dto.cur_epoch:
        command.extend(["--cur-epoch", str(dto.cur_epoch)])
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    dto = KeytoolGenerateDTO(**data)
    command = ["keytool", "generate", dto.key_scheme]
    if dto.derivation_path:
        command.append(dto.derivation_path)
    if dto.word_length:
        command.append(dto.word_length)
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/import", methods=["POST"])
def import_key():
    data = request.get_json()
    dto = KeytoolImportDTO(**data)
    command = ["keytool", "import", dto.input_string, dto.key_scheme]
    if dto.derivation_path:
        command.append(dto.derivation_path)
    if dto.alias:
        command.extend(["--alias", dto.alias])
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    dto = KeytoolExportDTO(**data)
    command = ["keytool", "export", "--key-identity", dto.key_identity]
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/list", methods=["GET"])
def list_keys():
    command = ["keytool", "list"]
    output = sui_command(command)
    return {"output": output}


@keytool_blueprint.route("/load-keypair", methods=["POST"])
def load_keypair():
    data = request.get_json()
    dto = KeytoolLoadKeypairDTO(**data)
    command = ["keytool", "load-keypair", dto.file]
    output = sui_command(command)
    return {"output": output}


@info_blueprint.route("/types", methods=["GET"])
def get_types():
    type_string = TypeDTO(name="string", is_array=False, is_choice=False)
    type_float = TypeDTO(name="float", is_array=False, is_choice=False)
    type_int = TypeDTO(name="int", is_array=False, is_choice=False)
    type_bool = TypeDTO(name="bool", is_array=False, is_choice=False)
    type_stringarray = TypeDTO(name="stringarray", is_array=True, is_choice=False)
    type_floatarray = TypeDTO(name="floatarray", is_array=True, is_choice=False)
    type_intarray = TypeDTO(name="intarray", is_array=True, is_choice=False)
    type_boolarray = TypeDTO(name="boolarray", is_array=True, is_choice=False)
    type_multichoice = TypeDTO(name="multichoice", is_array=False, is_choice=True)
    type_mark = TypeDTO(name="mark", is_array=False, is_choice=True)
    return jsonify(
        [
            type_string,
            type_float,
            type_int,
            type_bool,
            type_stringarray,
            type_floatarray,
            type_intarray,
            type_boolarray,
            type_multichoice,
            type_mark,
        ]
    )


@info_blueprint.route("/", methods=["GET"])
def get_info():
    file = open("all.json", "r")
    data = file.read()
    file.close()
    return data

@info_blueprint.route("/", methods=["POST"])
def get_specific_info():
    paths = request.json["paths"]
    file = open("all.json", "r")
    data = json.loads(file.read())
    for path in paths:
        data = data[path]
    return data
    
app.register_blueprint(client_blueprint, url_prefix="/client")
app.register_blueprint(keytool_blueprint, url_prefix="/keytool")
app.register_blueprint(start_blueprint, url_prefix="/start")
app.register_blueprint(info_blueprint, url_prefix="/info")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


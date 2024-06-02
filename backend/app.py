import json
import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from network import NetworkInitializer
from config import Config, NetworkType, NetworkDetails
from dto import (
    ClientBalanceDTO,
    KeytoolConvertDTO,
    ClientCallDTO,
    ClientPtbDTO,
    ClientPaySuiDTO,
    ClientExecuteCombinedSignedTxDTO,
    ClientPayDTO,
    ClientExecuteSignedTxDTO,
    ClientDynamicFieldDTO,
    ClientPayAllSuiDTO,
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
from utils import generic_command, sui_command, cat_command,sui_command_with_pipe

config = Config()
networkInitializer = NetworkInitializer(config.NETWORK_LOCATIONS)

app = Flask(__name__)


@app.route("/client/active-address", methods=["POST"])
def client_active_address():
    """
    Retrieves the active address of the client.

    Returns:
        dict: A dictionary containing the active address.
            Example: {"active_address": "123 Main St"}
    """
    response = sui_command(["client", "active-address"])
    return {"active_address": response}


@app.route("/client/active-env", methods=["POST"])
def client_active_env():
    response = sui_command(["client", "active-env"])
    return {"active_env": response}


@app.route("/client/addresses", methods=["POST"])
def client_addresses():
    response = sui_command(["client", "addresses"])
    return response


@app.route("/client/balance", methods=["POST"])
def client_balance():
    data = ClientBalanceDTO(**request.json)
    command = ["client", "balance", data.address]
    if data.coin_type:
        command.extend(["--coin-type", data.coin_type])
    if data.with_coins:
        command.append("--with-coins")
    response = sui_command(command)
    return jsonify(response)


@app.route("/client/call", methods=["POST"])
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
        "--gas-budPOST",
        data.gas_budPOST,
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
    if data.gas_budPOST:
        command.extend(["--gas-budPOST", data.gas_budPOST])
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


@app.route("/client/chain-identifier", methods=["POST"])
def client_chain_identifier():
    command = ["client", "chain-identifier"]
    response = sui_command(command)
    return response


@app.route("/client/dynamic-field", methods=["POST"])
def client_dynamic_field():
    data = ClientDynamicFieldDTO(**request.json)
    command = ["client", "dynamic-field", data.object_id]
    if data.cursor:
        command.extend(["--cursor", data.cursor])
    if data.limit:
        command.extend(["--limit", str(data.limit)])
    response = sui_command(command)
    return response


@app.route("/client/envs", methods=["POST"])
def client_envs():
    try:
        command = ["client", "envs"]
        response = sui_command(command)
        return jsonify(response)
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/client/execute-signed-tx", methods=["POST"])
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


@app.route("/client/execute-combined-signed-tx", methods=["POST"])
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


@app.route("/client/faucet", methods=["POST"])
def client_faucet():
    network = sui_command(["client", "active-env"])
    address = sui_command(["client", "active-address"])
    network = config.NETWORK_LOCATIONS[network][NetworkDetails.GasFaucetUrl]
    print(
        requests.post(
            network + "/gas", json={"FixedAmountRequest": {"recipient": address}}
        ).json()
    )
    return requests.post(
        network + "/gas", json={"FixedAmountRequest": {"recipient": address}}
    ).json()


@app.route("/client/gas", methods=["POST"])
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


@app.route("/client/merge-coin", methods=["POST"])
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
            "--gas-budPOST",
            data.gas_budPOST,
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


@app.route("/client/new-address", methods=["POST"])
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


@app.route("/client/object", methods=["POST"])
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


@app.route("/client/objects", methods=["POST"])
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


@app.route("/client/pay", methods=["POST"])
def client_pay():
    try:
        data = ClientPayDTO(**request.json)
        command = ["client", "pay", "--gas-budPOST", data.gas_budPOST]
        command.extend(["--input-coins"] + data.input_coins)
        command.extend(["--recipients"] + data.recipients)
        command.extend(["--amounts"] + data.amounts)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/client/pay-all-sui", methods=["POST"])
def client_pay_all_sui():
    try:
        data = ClientPayAllSuiDTO(**request.json)
        command = [
            "client",
            "pay-all-sui",
            "--recipient",
            data.recipient,
            "--gas-budPOST",
            data.gas_budPOST,
        ]
        command.extend(["--input-coins"] + data.input_coins)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/client/pay-sui", methods=["POST"])
def client_pay_sui():
    try:
        data = ClientPaySuiDTO(**request.json)
        command = ["client", "pay-sui", "--gas-budPOST", data.gas_budPOST]
        command.extend(["--input-coins"] + data.input_coins)
        command.extend(["--recipients"] + data.recipients)
        command.extend(["--amounts"] + data.amounts)
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/client/ptb", methods=["POST"])
def client_ptb():
    try:
        data = ClientPtbDTO(**request.json)
        command = ["client", "ptb"]
        if data.assign:
            for name, value in data.assign.items():
                command.extend(["--assign", name, value])
        if data.gas_coin:
            command.extend(["--gas-coin", data.gas_coin])
        if data.gas_budPOST:
            command.extend(["--gas-budPOST", data.gas_budPOST])
        # Add similar checks for other options...
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/client/publish", methods=["POST"])
def client_publish():
    data = ClientPublishDTO(**request.json)
    command = ["client", "publish", "--gas-budPOST", data.gas_budPOST]
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


@app.route("/client/split-coin", methods=["POST"])
def client_split_coin():
    data = ClientSplitCoinDTO(**request.json)
    command = [
        "client",
        "split-coin",
        "--coin-id",
        data.coin_id,
        "--gas-budPOST",
        data.gas_budPOST,
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


@app.route("/client/switch", methods=["POST"])
def client_switch():
    data = ClientSwitchDTO(**request.json)
    command = ["client", "switch"]
    if data.address:
        command.extend(["--address", data.address])
    if data.env:
        command.extend(["--env", data.env])
    response = sui_command(command)
    return response


@app.route("/client/tx-block", methods=["POST"])
def client_tx_block():
    data = ClientTxBlockDTO(**request.json)
    command = ["client", "tx-block", data.digest]
    response = sui_command(command)
    return response


@app.route("/client/transfer", methods=["POST"])
def client_transfer():
    data = ClientTransferDTO(**request.json)
    command = [
        "client",
        "transfer",
        "--to",
        data.to,
        "--object-id",
        data.object_id,
        "--gas-budPOST",
        data.gas_budPOST,
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


@app.route("/client/transfer-sui", methods=["POST"])
def client_transfer_sui():
    data = ClientTransferSuiDTO(**request.json)
    command = [
        "client",
        "transfer-sui",
        "--to",
        data.to,
        "--sui-coin-object-id",
        data.sui_coin_object_id,
        "--gas-budPOST",
        data.gas_budPOST,
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


@app.route("/client/upgrade", methods=["POST"])
def client_upgrade():
    data = ClientUpgradeDTO(**request.json)
    command = [
        "client",
        "upgrade",
        "--upgrade-capability",
        data.upgrade_capability,
        "--gas-budPOST",
        data.gas_budPOST,
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


@app.route("/client/verify-bytecode-meter", methods=["POST"])
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


@app.route("/client/verify-source", methods=["POST"])
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


@app.route("/client/profile-transaction", methods=["POST"])
def client_profile_transaction():
    data = ClientProfileTransactionDTO(**request.json)
    command = ["client", "profile-transaction", "--tx-digest", data.tx_digest]
    if data.profile_output:
        command.extend(["--profile-output", data.profile_output])
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@app.route("/client/replay-transaction", methods=["POST"])
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


@app.route("/client/replay-batch", methods=["POST"])
def client_replay_batch():
    data = ClientReplayBatchDTO(**request.json)
    command = ["client", "replay-batch", "--path", data.path]
    if data.terminate_early:
        command.append("--terminate-early")
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@app.route("/client/replay-checkpoint", methods=["POST"])
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


@app.route("/client/private", methods=["POST"])
def client_private():
    response = cat_command(
        "~/.sui/sui_config/sui.keystore", isJson=True, name="private_key"
    )
    return {"private_keys": response}


#### KEYTOOL ENDPOINTS ####


@app.route("/keytool/update-alias", methods=["POST"])
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


@app.route("/keytool/convert", methods=["POST"])
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


@app.route("/keytool/decode-or-verify-tx", methods=["POST"])
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


@app.route("/keytool/decode-multi-sig", methods=["POST"])
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


@app.route("/keytool/generate", methods=["POST"])
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


@app.route("/keytool/import", methods=["POST"])
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


@app.route("/keytool/export", methods=["POST"])
def export():
    data = request.get_json()
    dto = KeytoolExportDTO(**data)
    command = ["keytool", "export", "--key-identity", dto.key_identity]
    output = sui_command(command)
    return {"output": output}


@app.route("/keytool/list", methods=["POST"])
def list_keys():
    command = ["keytool", "list"]
    output = sui_command(command)
    return {"output": output}


@app.route("/keytool/load-keypair", methods=["POST"])
def load_keypair():
    data = request.get_json()
    dto = KeytoolLoadKeypairDTO(**data)
    command = ["keytool", "load-keypair", dto.file]
    output = sui_command(command)
    return {"output": output}


@app.route("/command/types", methods=["POST"])
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


@app.route("/command/all", methods=["POST"])
def get_info():
    file = open("all.json", "r")
    data = file.read()
    file.close()
    return data


@app.route("/command", methods=["POST"])
def get_specific_info():
    paths = request.json["paths"]
    file = open("all.json", "r")
    data = json.loads(file.read())
    for path in paths:
        data = data[path]
    return data


@app.route("/network/check-local-network", methods=["POST"])
def check_local_network():
    command = [
        "client",
        "new-env",
        "--alias",
        "local",
        "--rpc",
        config.NETWORK_LOCATIONS[NetworkType.Local][NetworkDetails.RpcEndpoint],
    ]
    try:
        response = sui_command(command, False, "output")
        print(response)
        if "error" in response["output"]:
            return {"error": "Local network not found"}, 400
    except Exception as e:
        print(e)
        return {"error": "Local network not found"}, 400
    return response


@app.route("/network/details", methods=["POST"])
def get_network_details():
    """
    Retrieves the network details.

    Returns:
        A JSON response containing the network locations.
    """
    return jsonify(config.network_locations)


@app.route("/move/create", methods=["POST"])
def create_move():
    data = request.get_json()
    command = ["move", "new", "--path", f"projects/{data['projectName']}", data['projectName']]
    sui_command(command, isJson=False, name="output")
    source_file_path = f"projects/{data['projectName']}/sources/{data['projectName']}.move"
    test_file_path = f"projects/{data['projectName']}/tests/{data['projectName']}_tests.move"
    toml_path = "projects/" + data['projectName'] + "/Move.toml"
    with open(source_file_path, "r") as file:
        lines = file.readlines()
    lines = lines[2:-1]
    with open(source_file_path, "w") as file:
        file.writelines(lines)
    with open(test_file_path, "r") as file:
        lines = file.readlines()
    lines = lines[2:-1]
    with open(test_file_path, "w") as file:
        file.writelines(lines)
    test_path = "projects/" + data['projectName'] + "/tests"
    source_path = "projects/" + data['projectName'] + "/sources"
    tests = generic_command("ls " + test_path).decode("utf-8")
    toml_file = generic_command("cat " + toml_path).decode("utf-8")
    test_file_list = [test for test in tests.split("\n") if test]
    source_files = generic_command("ls " + source_path).decode("utf-8")
    source_file_list = [source for source in source_files.split("\n") if source]
    test_dict = {
        test_file_name: generic_command(f"cat {test_path}/{test_file_name}").decode("utf-8")
        for test_file_name in test_file_list
    }
    source_dict = {
        source_file_name: generic_command(f"cat {source_path}/{source_file_name}").decode("utf-8")
        for source_file_name in source_file_list
    }
    return {"tests": test_dict, "sources": source_dict, "toml": toml_file}


@app.route("/move/list", methods=["POST"])
def list_move_projects():
    if not os.path.exists("projects"):
        return {"projects": []}
    projects_dir = "projects"
    projects = os.listdir(projects_dir)
    projects_info = []
    for project in projects:
        project_path = os.path.join(projects_dir, project)
        modification_time = os.path.getmtime(project_path)
        readable_time = time.ctime(modification_time)
        projects_info.append({"name": project, "last_updated": readable_time})
    return {"projects": projects_info}

@app.route("/move/delete", methods=["POST"])
def delete_move():
    data = request.get_json()
    command = ["rm", "-r", data['projectName']]
    generic_command(command)
    return "Delet1ed successfully"

@app.route("/move/update", methods=["POST"])
def update_move():
    data = request.get_json()
    projectName = data['projectName']
    fileName = data["fileName"]
    fileContent = data["fileContent"]
    project_path = f"projects/{projectName}"
    sources_path = f"{project_path}/sources"
    tests_path = f"{project_path}/tests"
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Project {projectName} not found")

    if "_tests" in fileName:
        file_path = f"{tests_path}/{fileName}"
    else:
        file_path = f"{sources_path}/{fileName}"
    with open(file_path, "w") as file:
        file.write(fileContent)
    return "Updated successfully", 200


@app.route("/move/open", methods=["POST"])
def open_move():
    data = request.get_json()
    project_name = data['projectName']
    project_path = f"projects/{project_name}"
    sources_path = f"{project_path}/sources"
    tests_path = f"{project_path}/tests"
    sources = generic_command(f"ls {sources_path}").decode("utf-8")
    tests = generic_command(f"ls {tests_path}").decode("utf-8")
    toml_file = generic_command(f"cat {project_path}/Move.toml").decode("utf-8")
    test_list = [test for test in tests.split("\n") if test]
    source_list = [source for source in sources.split("\n") if source]
    test_dict = {
        test: generic_command(f"cat {tests_path}/{test}").decode("utf-8")
        for test in test_list
    }
    source_dict = {
        source: generic_command(f"cat {sources_path}/{source}").decode(
            "utf-8"
        )
        for source in source_list
    }
    return {"tests": test_dict, "sources": source_dict, "toml": toml_file}


@app.route("/move/build", methods=["POST"])
def build_move():
    data = request.get_json()
    project_name = data['projectName']
    path = os.getcwd()
    command = ["move", "build", "--path", f"{path}/projects/{project_name}"]
    output = sui_command(command, isJson=False, name="output")
    return output


@app.route("/move/test", methods=["POST"])
def test_move():
    data = request.get_json()
    project_name = data['projectName']
    path = os.getcwd()
    command = ["move", "test", "--path", f"{path}/projects/{project_name}"]
    output = sui_command_with_pipe(command, isJson=False)
    return jsonify(output)

@app.route("/move/publish", methods=["POST"])
def publish_move():
    data = request.get_json()
    project_name = data['projectName']
    budget = data["budget"]
    path = os.getcwd()
    command = ["client", "publish", 
               f"{path}/projects/{project_name}",
               "--gas-budget",     
               budget, 
               "--skip-dependency-verification"]
    output = sui_command_with_pipe(command, isJson=True)
    return jsonify(output)

cors = CORS(app, resource={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
networkInitializer.init_networks()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=7777)

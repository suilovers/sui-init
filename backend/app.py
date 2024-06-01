import json
from os import listdir
import os
import subprocess
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
from utils import generic_command, sui_command, cat_command

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
def current_balance():
    response = sui_command(["client", "balance"])
    return jsonify(response)


@app.route("/client/balance", methods=["POST"])
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
        response = sui_command(command), 200
    except:
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
    command = ["move", "new", data["projectName"]]
    output = sui_command(command, isJson=False, name="output")
    os.mkdir(data["projectName"]+"/tests")
    sources = ["main.move"]
    tests = ["main.move"]
    for source in sources:
        source_file = open(data["projectName"] + "/sources/" + source, "w")
        source_file.write("""module 0x1::MyModule {
    public fun hello_world() {
        debug::print("Hello, Move!");
    }
}
""")
        source_file.close()
    for test in tests:
        test_file = open(data["projectName"] + "/tests/" + test, "w")
        test_file.write("""script {
    use 0x1::MyModule;

    fun test_hello_world() {
        MyModule::hello_world();
    }
}""")
        test_file.close()        
    sources = generic_command('ls '+data["projectName"]+'/sources').decode("utf-8")
    tests = generic_command('ls '+data["projectName"]+'/tests').decode("utf-8")
    toml_file = generic_command('cat '+data["projectName"]+'/Move.toml').decode("utf-8")
    test_list = [test for test in tests.split('\n') if test]
    source_list = [source for source in sources.split('\n') if source]
    test_dict = {test: generic_command('cat ' + data["projectName"] + '/tests/' + test).decode("utf-8") for test in test_list}
    source_dict = {source: generic_command('cat ' + data["projectName"] + '/sources/' + source).decode("utf-8") for source in source_list}
    return { "tests": test_dict, "sources": source_dict, "toml": toml_file}

@app.route("/move/save", methods=["POST"])
def save_move():
    data = request.get_json()
    project_name = data["projectName"]
    tests = {key: value.replace("\r", "") for key, value in data["tests"].items()}
    sources = {key: value.replace("\r", "") for key, value in data["sources"].items()}
    toml = data["toml"].replace("\r", "")
    # save toml file
    toml_file = open(project_name + "/Move.toml", "w")
    toml_file.write(toml)
    toml_file.close()
    for source in sources:
        source_file = open(project_name + "/sources/" + source, "w")
        source_file.write(sources[source])
        source_file.close()
    # save tests
    for test in tests:
        test_file = open(project_name + "/tests/" + test, "w")
        test_file.write(tests[test])
        test_file.close()
    return "Saved successfully"

@app.route("/move/open", methods=["POST"])
def open_move():
    data = request.get_json()
    project_name = data["projectName"]
    sources = generic_command('ls '+project_name+'/sources').decode("utf-8")
    tests = generic_command('ls '+project_name+'/tests').decode("utf-8")
    toml_file = generic_command('cat '+project_name+'/Move.toml').decode("utf-8")
    test_list = [test for test in tests.split('\n') if test]
    source_list = [source for source in sources.split('\n') if source]
    test_dict = {test: generic_command('cat ' + project_name + '/tests/' + test).decode("utf-8") for test in test_list}
    source_dict = {source: generic_command('cat ' + project_name + '/sources/' + source).decode("utf-8") for source in source_list}
    return { "tests": test_dict, "sources": source_dict, "toml": toml_file}


@app.route("/move/build", methods=["POST"])
def build_move():
    data = request.get_json()
    project_name = data["projectName"]
    path = os.getcwd()
    command = ["move", "build", "--path" , path + "/" + project_name]
    output = sui_command(command, isJson=False, name="output")
    return {"output": output}


@app.route("/move/test", methods=["POST"])
def test_move():
    data = request.get_json()
    project_name = data["projectName"]
    path = os.getcwd()
    command = ["move", "test", "--path" , path + "/" + project_name]
    output = sui_command(command, isJson=False, name="output")
    return {"output": output}
cors = CORS(app, resource={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
networkInitializer.init_networks()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=7777)

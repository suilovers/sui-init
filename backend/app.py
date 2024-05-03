from flask import Blueprint, Flask, request, jsonify

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


@api_blueprint.route("/client/envs", methods=["GET"])
def client_envs():
    try:
        command = ["client", "envs"]
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


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


@api_blueprint.route("/client/faucet", methods=["GET"])
def client_faucet():
    try:
        data = ClientFaucetDTO(**request.args)
        command = ["client", "faucet"]
        if data.address:
            command.extend(["--address", data.address])
        if data.url:
            command.extend(["--url", data.url])
        response = sui_command(command)
        return response
    except ValidationError as e:
        return {"error": str(e)}, 400


@api_blueprint.route("/client/gas", methods=["GET"])
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


@api_blueprint.route("/client/merge-coin", methods=["POST"])
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


@api_blueprint.route("/client/new-address", methods=["POST"])
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


@api_blueprint.route("/client/object", methods=["GET"])
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


@api_blueprint.route("/client/objects", methods=["GET"])
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


@api_blueprint.route("/client/publish", methods=["POST"])
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


@api_blueprint.route("/client/split-coin", methods=["POST"])
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


@api_blueprint.route("/client/switch", methods=["POST"])
def client_switch():
    data = ClientSwitchDTO(**request.json)
    command = ["client", "switch"]
    if data.address:
        command.extend(["--address", data.address])
    if data.env:
        command.extend(["--env", data.env])
    response = sui_command(command)
    return response


@api_blueprint.route("/client/tx-block", methods=["POST"])
def client_tx_block():
    data = ClientTxBlockDTO(**request.json)
    command = ["client", "tx-block", data.digest]
    response = sui_command(command)
    return response


@api_blueprint.route("/client/transfer", methods=["POST"])
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


@api_blueprint.route("/client/transfer-sui", methods=["POST"])
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


@api_blueprint.route("/client/upgrade", methods=["POST"])
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


@api_blueprint.route("/client/verify-bytecode-meter", methods=["POST"])
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


@api_blueprint.route("/client/verify-source", methods=["POST"])
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


@api_blueprint.route("/client/profile-transaction", methods=["POST"])
def client_profile_transaction():
    data = ClientProfileTransactionDTO(**request.json)
    command = ["client", "profile-transaction", "--tx-digest", data.tx_digest]
    if data.profile_output:
        command.extend(["--profile-output", data.profile_output])
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@api_blueprint.route("/client/replay-transaction", methods=["POST"])
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


@api_blueprint.route("/client/replay-batch", methods=["POST"])
def client_replay_batch():
    data = ClientReplayBatchDTO(**request.json)
    command = ["client", "replay-batch", "--path", data.path]
    if data.terminate_early:
        command.append("--terminate-early")
    if data.json:
        command.append("--json")
    response = sui_command(command)
    return response


@api_blueprint.route("/client/replay-checkpoint", methods=["POST"])
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

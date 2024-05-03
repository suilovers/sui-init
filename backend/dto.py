from pydantic import BaseModel
from typing import List, Optional, Dict


class StartDTO(BaseModel):
    network_config: str = None
    no_full_node: bool = False


class ClientBalanceDTO(BaseModel):
    address: str
    coin_type: str = None
    with_coins: bool = False


class KeytoolConvertDTO(BaseModel):
    value: str


class ClientCallDTO(BaseModel):
    package: str
    module: str
    function: str
    gas_budget: str
    type_args: Optional[List[str]] = None
    args: Optional[List[str]] = None
    gas: Optional[str] = None
    dry_run: bool = False
    serialize_unsigned_transaction: bool = False
    serialize_signed_transaction: bool = False


class ClientDynamicFieldDTO(BaseModel):
    object_id: str
    cursor: Optional[str] = None
    limit: Optional[int] = 50


class ClientExecuteSignedTxDTO(BaseModel):
    tx_bytes: str
    signatures: List[str]


class ClientExecuteCombinedSignedTxDTO(BaseModel):
    signed_tx_bytes: str


class ClientNewEnvDTO(BaseModel):
    alias: str
    rpc: str
    ws: Optional[str]


class ClientPayDTO(BaseModel):
    input_coins: List[str]
    recipients: List[str]
    amounts: List[str]
    gas_budget: str


class ClientPayAllSuiDTO(BaseModel):
    input_coins: List[str]
    recipient: str
    gas_budget: str


class ClientPaySuiDTO(BaseModel):
    input_coins: List[str]
    recipients: List[str]
    amounts: List[str]
    gas_budget: str


class ClientPtbDTO(BaseModel):
    assign: Optional[Dict[str, str]]
    gas_coin: Optional[str]
    gas_budget: Optional[str]
    make_move_vec: Optional[Dict[str, List[str]]]
    merge_coins: Optional[Dict[str, List[str]]]
    move_call: Optional[Dict[str, str]]
    split_coins: Optional[Dict[str, List[str]]]
    transfer_objects: Optional[Dict[str, List[str]]]
    publish: Optional[str]
    upgrade: Optional[str]
    preview: Optional[bool]
    serialize_unsigned_transaction: Optional[bool]
    serialize_signed_transaction: Optional[bool]
    summary: Optional[bool]
    warn_shadows: Optional[bool]


class ClientFaucetDTO(BaseModel):
    address: Optional[str] = None
    url: Optional[str] = None


class ClientGasDTO(BaseModel):
    owner_address: Optional[str] = None


class ClientMergeCoinDTO(BaseModel):
    primary_coin: str
    coin_to_merge: str
    gas: Optional[str] = None
    gas_budget: str
    dry_run: bool = False
    serialize_unsigned_transaction: bool = False
    serialize_signed_transaction: bool = False


class ClientNewAddressDTO(BaseModel):
    key_scheme: str
    alias: Optional[str] = None
    word_length: Optional[str] = None
    derivation_path: Optional[str] = None


class ClientObjectDTO(BaseModel):
    object_id: str
    bcs: bool = False


class ClientObjectsDTO(BaseModel):
    owner_address: Optional[str] = None


class ClientPublishDTO(BaseModel):
    package_path: Optional[str] = "."
    dev: Optional[bool] = False
    test: Optional[bool] = False
    doc: Optional[bool] = False
    install_dir: Optional[str] = None
    force: Optional[bool] = False
    fetch_deps_only: Optional[bool] = False
    skip_fetch_latest_git_deps: Optional[bool] = False
    default_move_flavor: Optional[str] = None
    default_move_edition: Optional[str] = None
    dependencies_are_root: Optional[bool] = False
    silence_warnings: Optional[bool] = False
    warnings_are_errors: Optional[bool] = False
    no_lint: Optional[bool] = False
    lint: Optional[bool] = False
    gas: Optional[str] = None
    gas_budget: str
    dry_run: Optional[bool] = False
    serialize_unsigned_transaction: Optional[bool] = False
    serialize_signed_transaction: Optional[bool] = False
    skip_dependency_verification: Optional[bool] = False
    with_unpublished_dependencies: Optional[bool] = False


class ClientSplitCoinDTO(BaseModel):
    coin_id: str
    amounts: Optional[List[int]] = None
    count: Optional[int] = None
    gas: Optional[str] = None
    gas_budget: str
    dry_run: Optional[bool] = False
    serialize_unsigned_transaction: Optional[bool] = False
    serialize_signed_transaction: Optional[bool] = False


class ClientSwitchDTO(BaseModel):
    address: Optional[str] = None
    env: Optional[str] = None


class ClientTxBlockDTO(BaseModel):
    digest: str


class ClientTransferDTO(BaseModel):
    to: str
    object_id: str
    gas: Optional[str] = None
    gas_budget: str
    dry_run: Optional[bool] = False
    serialize_unsigned_transaction: Optional[bool] = False
    serialize_signed_transaction: Optional[bool] = False


class ClientTransferSuiDTO(BaseModel):
    to: str
    sui_coin_object_id: str
    gas_budget: str
    amount: Optional[str] = None
    dry_run: Optional[bool] = False
    serialize_unsigned_transaction: Optional[bool] = False
    serialize_signed_transaction: Optional[bool] = False


class ClientUpgradeDTO(BaseModel):
    upgrade_capability: str
    gas_budget: str
    package_path: Optional[str] = "."
    dev: Optional[bool] = False
    test: Optional[bool] = False
    doc: Optional[bool] = False
    install_dir: Optional[str] = None
    force: Optional[bool] = False
    fetch_deps_only: Optional[bool] = False
    skip_fetch_latest_git_deps: Optional[bool] = False
    default_move_flavor: Optional[str] = None
    default_move_edition: Optional[str] = None
    dependencies_are_root: Optional[bool] = False
    silence_warnings: Optional[bool] = False
    warnings_are_errors: Optional[bool] = False
    no_lint: Optional[bool] = False
    lint: Optional[bool] = False
    gas: Optional[str] = None
    dry_run: Optional[bool] = False
    serialize_unsigned_transaction: Optional[bool] = False
    serialize_signed_transaction: Optional[bool] = False
    skip_dependency_verification: Optional[bool] = False
    with_unpublished_dependencies: Optional[bool] = False


class ClientVerifyBytecodeMeterDTO(BaseModel):
    package: Optional[str] = "."
    protocol_version: Optional[str] = None
    module: Optional[List[str]] = None
    dev: Optional[bool] = False
    test: Optional[bool] = False
    doc: Optional[bool] = False
    install_dir: Optional[str] = None
    force: Optional[bool] = False
    fetch_deps_only: Optional[bool] = False
    skip_fetch_latest_git_deps: Optional[bool] = False
    default_move_flavor: Optional[str] = None
    default_move_edition: Optional[str] = None
    dependencies_are_root: Optional[bool] = False
    silence_warnings: Optional[bool] = False
    warnings_are_errors: Optional[bool] = False
    no_lint: Optional[bool] = False
    lint: Optional[bool] = False


class ClientVerifySourceDTO(BaseModel):
    package_path: Optional[str] = "."
    dev: Optional[bool] = False
    test: Optional[bool] = False
    doc: Optional[bool] = False
    install_dir: Optional[str] = None
    force: Optional[bool] = False
    fetch_deps_only: Optional[bool] = False
    skip_fetch_latest_git_deps: Optional[bool] = False
    default_move_flavor: Optional[str] = None
    default_move_edition: Optional[str] = None
    dependencies_are_root: Optional[bool] = False
    silence_warnings: Optional[bool] = False
    warnings_are_errors: Optional[bool] = False
    no_lint: Optional[bool] = False
    lint: Optional[bool] = False
    verify_deps: Optional[bool] = False
    skip_source: Optional[bool] = False
    address_override: Optional[str] = None


class ClientVerifySourceDTO(BaseModel):
    package_path: Optional[str] = "."
    dev: Optional[bool] = False
    test: Optional[bool] = False
    doc: Optional[bool] = False
    install_dir: Optional[str] = None
    force: Optional[bool] = False
    fetch_deps_only: Optional[bool] = False
    skip_fetch_latest_git_deps: Optional[bool] = False
    default_move_flavor: Optional[str] = None
    default_move_edition: Optional[str] = None
    dependencies_are_root: Optional[bool] = False
    silence_warnings: Optional[bool] = False
    warnings_are_errors: Optional[bool] = False
    no_lint: Optional[bool] = False
    lint: Optional[bool] = False
    verify_deps: Optional[bool] = False
    skip_source: Optional[bool] = False
    address_override: Optional[str] = None


class ClientProfileTransactionDTO(BaseModel):
    tx_digest: str
    profile_output: Optional[str] = None


class ClientReplayTransactionDTO(BaseModel):
    tx_digest: str
    gas_info: Optional[bool] = False
    ptb_info: Optional[bool] = False
    executor_version: Optional[str] = None
    protocol_version: Optional[str] = None


class ClientReplayBatchDTO(BaseModel):
    path: str
    terminate_early: Optional[bool] = False


class ClientReplayCheckpointDTO(BaseModel):
    start: int
    end: int
    terminate_early: Optional[bool] = False

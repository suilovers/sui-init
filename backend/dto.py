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
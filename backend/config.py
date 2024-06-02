import os

from dotenv import load_dotenv


class NetworkType:
    """
    Represents the different network types.

    Attributes:
        Local (str): Represents the local network.
        Devnet (str): Represents the Devnet network.
        Testnet (str): Represents the Testnet network.
        Mainnet (str): Represents the Mainnet network.
    """

    Local = "local"
    Devnet = "Devnet"
    Testnet = "Testnet"
    Mainnet = "Mainnet"


class NetworkDetails:
    RpcEndpoint = "rpc_endpoint"
    GasFaucetUrl = "gas_faucet_url"

class Config:
    def __init__(self):
        """
        Initializes the Config class.

        Loads variables from the .env file and sets up network locations for different network types.
        """
        env = os.getenv("ENV", "production")
        
        env_file = f'.env.{env}'
        print(f"ENV: {env_file}")
        if os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            raise FileNotFoundError(f"File {env_file} not found")
        self.network_locations = {
            NetworkType.Local: {
                "rpc_endpoint": os.getenv("LOCAL_RPC_ENDPOINT"),
                "gas_faucet_url": os.getenv("LOCAL_GAS_FAUCET_URL"),
            },
            NetworkType.Devnet: {
                "rpc_endpoint": os.getenv("DEVNET_RPC_ENDPOINT"),
                "gas_faucet_url": os.getenv("DEVNET_GAS_FAUCET_URL"),
            },
            NetworkType.Testnet: {
                "rpc_endpoint": os.getenv("TESTNET_RPC_ENDPOINT"),
                "gas_faucet_url": os.getenv("TESTNET_GAS_FAUCET_URL"),
            },
            NetworkType.Mainnet: {
                "rpc_endpoint": os.getenv("MAINNET_RPC_ENDPOINT"),
                "gas_faucet_url": os.getenv("MAINNET_GAS_FAUCET_URL"),
            },
        }

    @property
    def NETWORK_LOCATIONS(self):
        """
        Returns the network locations.

        Returns:
            list: A list of network locations.
        """
        return self.network_locations

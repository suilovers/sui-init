from utils import sui_command
from config import NetworkDetails, NetworkType


class NetworkInitializer:
    def __init__(self, networkLocations: dict[str, dict[str, str | None]]) -> None:
        """
        Initializes the NetworkInitializer class.

        Args:
            networkLocations (dict[str, dict[str, str | None]]): A dictionary containing network locations.
        """
        self.network_locations = networkLocations

    def init_networks(self):
        """
        Initializes the networks.

        Returns:
            dict: A dictionary containing network locations.
        """
        print("Initializing networks...")
        for [networkAlias, network] in self.network_locations.items():
            if network[NetworkDetails.RpcEndpoint] is None:
                raise Exception(f"RPC endpoint for {network} is not set.")
            if network[NetworkDetails.RpcEndpoint] is None:
                raise Exception(f"Gas faucet URL for {network} is not set.")
            sui_command
            print(f"Initializing {networkAlias} network...")
            command = [
                "client",
                "new-env",
                "--alias",
                networkAlias,
                "--rpc",
                network[NetworkDetails.RpcEndpoint],
            ]
            try:
                sui_command(command)
            except Exception as e:
                print(f"Error initializing {networkAlias} network: {e}")
                continue

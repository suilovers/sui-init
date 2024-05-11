export const API_BASE_URL = 'http://127.0.0.1:5000';

export enum CallStatus {
    LOADING,
    SUCCESS,
    ERROR
}

type EnvironmentData = {
    fullNodeUrl: string;
    gasFaucetUrl: string | null;
};

type Environments = {
    [key: string]: EnvironmentData;
};

export const NetworkLocations: Environments = {
    local: {
        fullNodeUrl: 'http://127.0.0.1:9000',
        gasFaucetUrl: 'http://127.0.0.1:9123/gas'
    },
    Devnet: {
        fullNodeUrl: 'https://fullnode.devnet.sui.io:443',
        gasFaucetUrl: 'https://faucet.devnet.sui.io/gas'
    },
    Testnet: {
        fullNodeUrl: 'https://fullnode.testnet.sui.io:443',
        gasFaucetUrl: 'https://faucet.testnet.sui.io/gas'
    },
    Mainnet: {
        fullNodeUrl: 'https://fullnode.mainnet.sui.io:443',
        gasFaucetUrl: null
    }
};

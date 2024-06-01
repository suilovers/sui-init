export const API_BASE_URL = 'http://127.0.0.1:7777';

export enum CallStatus {
    LOADING,
    SUCCESS,
    ERROR
}

export enum NetworkType {
    Local = 'local',
    Devnet = 'Devnet',
    Testnet = 'Testnet',
    Mainnet = 'Mainnet'
}

export type EnvironmentData = {
    title: string;
    fullNodeUrl: string;
    gasFaucetUrl: string | null;
};

type Environments = {
    [key in NetworkType]: EnvironmentData;
};

export const NetworkLocations: Environments = {
    [NetworkType.Local]: {
        title: 'Local',
        fullNodeUrl: 'http://127.0.0.1:8000',
        gasFaucetUrl: 'http://127.0.0.1:9123/gas'
    },
    [NetworkType.Devnet]: {
        title: 'Devnet',
        fullNodeUrl: 'https://fullnode.devnet.sui.io:443',
        gasFaucetUrl: 'https://faucet.devnet.sui.io/gas'
    },
    [NetworkType.Testnet]: {
        title: 'Testnet',
        fullNodeUrl: 'https://fullnode.testnet.sui.io:443',
        gasFaucetUrl: 'https://faucet.testnet.sui.io/gas'
    },
    [NetworkType.Mainnet]: {
        title: 'Mainnet',
        fullNodeUrl: 'https://fullnode.mainnet.sui.io:443',
        gasFaucetUrl: null
    }
};

export const SuiScanUrlMap: { [key in NetworkType]: string } = {
    [NetworkType.Local]: `https://custom.suiscan.xyz/custom/home/?network=${encodeURIComponent(NetworkLocations.local.fullNodeUrl)}`,
    [NetworkType.Devnet]: 'https://suiscan.xyz/devnet/home',
    [NetworkType.Testnet]: 'https://suiscan.xyz/testnet/home',
    [NetworkType.Mainnet]: 'https://suiscan.xyz/mainnet/home'
};

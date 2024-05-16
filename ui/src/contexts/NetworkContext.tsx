import React, { useEffect } from 'react';
import { NetworkType } from '../config';
import { switchNetwork } from '../services/SuiService';

type NetworkContextType = {
    currentNetwork: NetworkType;
    setCurrentNetwork: (network: NetworkType) => void;
};

export const NetworkContextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [currentNetwork, setCurrentNetwork] = React.useState<NetworkType>(() => {
        const savedNetwork = localStorage.getItem('currentNetwork');
        return savedNetwork ? (savedNetwork as NetworkType) : NetworkType.Mainnet;
    });

    useEffect(() => {
        const savedNetwork = localStorage.getItem('currentNetwork');
        localStorage.setItem('currentNetwork', currentNetwork);

        async function handleNetworkChange() {
            try {
                await switchNetwork(currentNetwork);
                // refresh page
                window.location.reload();
            } catch (error) {
                console.error('Failed to switch network', error);
            }
        }
        if (currentNetwork !== savedNetwork) {
            handleNetworkChange();
        }
    }, [currentNetwork]);
    return <NetworkContext.Provider value={{ currentNetwork, setCurrentNetwork }}>{children}</NetworkContext.Provider>;
};

export const NetworkContext = React.createContext<NetworkContextType | undefined>(undefined);

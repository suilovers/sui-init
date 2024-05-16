import { useContext } from 'react';
import { NetworkContext } from '../contexts/NetworkContext';

export default function useSwitchNetwork() {
    const networkContext = useContext(NetworkContext);
    if (!networkContext) {
        throw new Error('useSwitchNetwork must be used within a NetworkContextProvider');
    }
    const { currentNetwork, setCurrentNetwork } = networkContext;
    return {
        currentNetwork,
        setCurrentNetwork
    };
}

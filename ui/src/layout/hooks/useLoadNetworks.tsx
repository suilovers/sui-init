import { useEffect, useState } from 'react';
import { CallStatus, EnvironmentData, NetworkLocations } from '../../config';
import { checkLocalNetwork } from '../../services/SuiService';

/**
 * Filters out the 'local' network from the given array of networks.
 *
 * @param networks - The array of networks to filter.
 * @returns The filtered array of networks without the 'local' network.
 */
const withoutLocal = (networks: [string, EnvironmentData][]) => networks.filter(([key]) => key !== 'local');
/**
 * Custom hook to load networks and their status.
 * @returns An object containing the loaded networks and their status.
 */
export function useLoadNetworks() {
    const [networks, setNetworks] = useState<[string, EnvironmentData][]>(Object.entries(NetworkLocations));
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);

    const localNetwork = NetworkLocations.local;
    useEffect(() => {
        const checkNetworks = async () => {
            try {
                const isNetworkAvailable = await checkLocalNetwork();
                if (isNetworkAvailable) {
                    setNetworks(Object.entries(NetworkLocations));
                    setStatus(CallStatus.SUCCESS);
                } else {
                    setNetworks(withoutLocal(Object.entries(NetworkLocations)));
                }
            } catch (error) {
                setNetworks(withoutLocal(Object.entries(NetworkLocations)));
                setStatus(CallStatus.ERROR);
            }
        };

        // Call the function immediately
        checkNetworks();

        // Then continue calling it at the specified interval
        const intervalId = setInterval(checkNetworks, 5000); // 5000 milliseconds = 5 seconds

        return () => clearInterval(intervalId);
    }, [localNetwork]);

    return { networks, status };
}

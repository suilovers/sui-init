import { Box } from '@mui/material';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { NetworkType } from '../config';
import useSwitchNetwork from '../hooks/useSwitchNetwork';
import { useLoadNetworks } from './hooks/useLoadNetworks';

export default function CustomSwitchEnvDropdown() {
    const { setCurrentNetwork, currentNetwork } = useSwitchNetwork();
    // convert object to array
    const { networks, status } = useLoadNetworks();
    const handleChange = (event: SelectChangeEvent) => {
        setCurrentNetwork(event.target.value as NetworkType);
    };
    return (
        <Box
            sx={{
                width: 200
            }}
        >
            <FormControl fullWidth size="small">
                <InputLabel id="network-label">Networks</InputLabel>
                <Select labelId="network-label" id="network" value={currentNetwork} label="Networks" onChange={handleChange}>
                    {networks.map(([key, network]) => (
                        <MenuItem value={key}>{network.title}</MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Box>
    );
}

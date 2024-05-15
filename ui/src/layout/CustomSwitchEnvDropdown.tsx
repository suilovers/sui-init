import { Box } from '@mui/material';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import * as React from 'react';
import { NetworkType } from '../config';
import { useLoadNetworks } from './hooks/useLoadNetworks';

export default function CustomSwitchEnvDropdown() {
    const [age, setAge] = React.useState('');
    // convert object to array
    const { networks, status } = useLoadNetworks();
    const handleChange = (event: SelectChangeEvent) => {
        console.log(event.target.value);
        setAge(event.target.value as string);
    };
    return (
        <Box
            sx={{
                width: 200
            }}
        >
            <FormControl fullWidth size="small">
                <InputLabel id="network-label">Networks</InputLabel>
                <Select labelId="network-label" id="network" value={age} label="Networks" onChange={handleChange} defaultValue={NetworkType.Mainnet}>
                    {networks.map(([key, network]) => (
                        <MenuItem defaultChecked={key === NetworkType.Mainnet} value={key}>
                            {network.title}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Box>
    );
}

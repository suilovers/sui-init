import React from 'react';
import { FormControl, Input, Button, Box } from '@mui/material';

function CustomForm({ buttonLabel, placeholder, run, changeInput }: {buttonLabel: string, placeholder: string, run: () => void, changeInput: (e: any) => void}) {
    return (
        <Box sx={{ padding: 2, backgroundColor: '#2a2a2a', borderRadius: 1 }}>
            <FormControl sx={{  padding: 2, borderRadius: 1 }}>
                <Input
                    placeholder={placeholder}
                    sx={{
                        marginBottom: 2,
                        padding: 0.5,
                        border: '2px solid #5f5f5f',
                        borderRadius: 1
                    }}
                    onChange={changeInput}
                />
                <Button variant="contained" color="primary" onClick={run}>
                    {buttonLabel}
                </Button>
            </FormControl>
        </Box>
    );
}

export default CustomForm;
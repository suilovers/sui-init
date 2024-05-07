import { Button, FormControl, TextField } from '@mui/material';
import { useState } from 'react';
import { useLoadCommand } from './hooks/useLoadCommand';
import { useSubmitCall } from './hooks/useSubmitCall';

export default function CommandExecutionView() {
    const { command, status } = useLoadCommand();
    const { status: callStatus, submitCall } = useSubmitCall(command?.path as string);

    const [values, setValues] = useState({
        name: '',
        email: ''
    });

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValues({
            ...values,
            [event.target.name]: event.target.value
        });
    };

    return (
        <form
            onSubmit={(e) => {
                e.preventDefault();
                submitCall();
            }}
        >
            <FormControl fullWidth>
                <TextField name="name" label="Name" value={values.name} onChange={handleChange} />
                <TextField name="email" label="Email" value={values.email} onChange={handleChange} />
                <Button type="submit" variant="contained" color="primary">
                    Submit
                </Button>
            </FormControl>
        </form>
    );
}

import { Alert, Button, FormControl, FormHelperText, Snackbar, TextField, Theme, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { useState } from 'react';
import { fetchCallWithArguments } from '../../services/SuiService';
import { CommandDTO } from '../../types/sui/response';

interface CommandExecutionFormProps {
    command: CommandDTO | null;
    onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}

const useStyles = makeStyles((theme: Theme) => ({
    root: {},
    formControl: {
        margin: theme.spacing(1),
        padding: theme.spacing(1),
        minWidth: 120
    },
    formGroupTitle: {
        margin: theme.spacing(1)
    },
    formButton: {
        padding: theme.spacing(1),
        margin: theme.spacing(2)
    }
}));

export default function CommandExecutionForm({ command, onSubmit }: CommandExecutionFormProps) {
    const [snackbarOpen, setOpen] = useState(false);
    const handleClose = (event: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpen(false);
    };
    const handleClick = async (event: any) => {
        const _path = command?.path;
        const _arguments: any = command?.arguments;
        const _options: any = command?.optionalArguments;
        const argumentValues = [];
        const optionValues = [];
        const argumentBodyNames = [];
        const optionsBodyNames = [];
        const form = event.target.form;
        for (let i = 0; i < form.length; i += 2) {
            if (form[i].value) {
                if (i < _arguments.length * 2) {
                    argumentValues.push(form[i].value);
                    argumentBodyNames.push(_arguments[i / 2].name);
                } else {
                    optionValues.push(form[i].value);
                    optionsBodyNames.push(_options[i / 2 - _arguments.length].name);
                }
            }
        }
        if (argumentValues.length === 0) {
            setOpen(true);
        } else {
            let isReturned = await fetchCallWithArguments(_path as string, argumentBodyNames, optionsBodyNames, argumentValues, optionValues);
            console.log(isReturned);
            if (!isReturned) {
                setOpen(true);
            } else {
                setOpen(false);
            }
        }
    };

    const classes = useStyles();
    return (
        <div className={classes.root}>
            <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleClose}>
                <Alert onClose={handleClose} severity="error" variant="filled" sx={{ width: '100%' }}>
                    Failed to send the command. Please check the arguments and try again.
                </Alert>
            </Snackbar>

            <form onSubmit={onSubmit}>
                <Typography variant="h6" component="div" className={classes.formGroupTitle}>
                    Arguments
                </Typography>
                {command?.arguments.map((argument, index) => (
                    <FormControl fullWidth className={classes.formControl} key={index}>
                        <TextField id="standard-basic" label={argument.name} variant="outlined" />
                        <FormHelperText id="my-helper-text">{argument.description}</FormHelperText>
                    </FormControl>
                ))}

                <Typography variant="h6" component="div" className={classes.formGroupTitle}>
                    Options
                </Typography>
                {command?.optionalArguments.map((option, index) => (
                    <FormControl fullWidth className={classes.formControl} key={index}>
                        <TextField id="standard-basic" label={option.name} variant="outlined" />
                        <FormHelperText id="my-helper-text">{option.description}</FormHelperText>
                    </FormControl>
                ))}
                <Button fullWidth onClick={handleClick} className={classes.formButton} variant="contained">
                    Send
                </Button>
            </form>
        </div>
    );
}

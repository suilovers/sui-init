import { Button, FormControl, FormHelperText, TextField, Theme, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { useShowSnackbar } from '../../hooks/useToggleSnackbar';
import { fetchCallWithArguments } from '../../services/SuiService';
import { CommandDTO } from '../../types/sui/response';

interface CommandExecutionFormProps {
    command: CommandDTO | null;
    onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
    setResponse: (response: Object) => void;
}

const useStyles = makeStyles((theme: Theme) => ({
    root: {},
    formControl: {
        margin: '8px 0 !important',
        padding: theme.spacing(1),
        minWidth: 120
    },
    formGroupTitle: {
        margin: '8px !important'
    },
    formButton: {
        padding: theme.spacing(1),
        marginTop: '16px !important'
    }
}));

export default function CommandExecutionForm({ command, onSubmit, setResponse }: CommandExecutionFormProps) {
    const { showMessage } = useShowSnackbar();
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
            showMessage({ message: 'Please fill the required fields.', severity: 'error' });
        } else {
            let response = await fetchCallWithArguments(_path as string, argumentBodyNames, optionsBodyNames, argumentValues, optionValues);
            if (!response) {
                showMessage({ message: 'Failed to send the command. Please check the arguments and try again.', severity: 'error' });
            } else {
                setResponse(response);
            }
        }
    };

    const classes = useStyles();
    return (
        <div className={classes.root}>
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

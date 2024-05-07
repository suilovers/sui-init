import { FormControl, FormHelperText, TextField, Theme, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { CommandDTO } from '../../types/sui/response';

interface CommandExecutionFormProps {
    command: CommandDTO | null;
    onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}

const useStyles = makeStyles((theme: Theme) => ({
    formControl: {
        margin: theme.spacing(1),
        padding: theme.spacing(1),
        minWidth: 120
    },
    formGroupTitle: {
        margin: theme.spacing(1)
    }
}));

export default function CommandExecutionForm({ command, onSubmit }: CommandExecutionFormProps) {
    const classes = useStyles();
    return (
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
        </form>
    );
}

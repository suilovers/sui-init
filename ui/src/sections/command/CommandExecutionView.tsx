import { Card, CardContent, Theme, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { CallStatus } from '../../config';
import CommandExecutionForm from './CommandExecutionForm';
import CommandExecutionResult from './CommandExecutionResult';
import { useDirectCall } from './hooks/useDirectCall';
import { useLoadCommand } from './hooks/useLoadCommand';
import { useSubmitCall } from './hooks/useSubmitCall';

const useStyles = makeStyles((theme: Theme) => ({
    cardRoot: {
        margin: "2rem 0",
        minWidth: 800
    }
}));
export default function CommandExecutionView() {
    const { command, status } = useLoadCommand();
    const classess = useStyles();
    const isRequiredForm = command?.arguments.length! > 0 || command?.optionalArguments.length! > 0;
    const { status: directCallStatus, response: directResponse } = useDirectCall(!isRequiredForm, command?.path);
    const { status: formCallStatus, onSubmit, response: formResponse } = useSubmitCall(command?.path as string);
    if (formCallStatus === CallStatus.SUCCESS || directCallStatus === CallStatus.SUCCESS) {
        return <CommandExecutionResult response={formResponse || directResponse} />;
    }

    if (isRequiredForm) {
        return (
            <Card className={classess.cardRoot}>
                <CardContent>
                    <Typography variant="h5" gutterBottom>
                        {command?.name}
                    </Typography>
                    <Typography color="text.secondary" variant="subtitle1" component="div">
                        {command?.description}
                    </Typography>
                    <CommandExecutionForm command={command} onSubmit={onSubmit} />
                </CardContent>
            </Card>
        );
    }

    return null;
}

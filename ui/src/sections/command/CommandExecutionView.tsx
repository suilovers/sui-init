import { Card, CardContent, Theme, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { useState } from 'react';
import { CallStatus } from '../../config';
import CommandExecutionForm from './CommandExecutionForm';
import CommandExecutionResult from './CommandExecutionResult';
import { useDirectCall } from './hooks/useDirectCall';
import { useLoadCommand } from './hooks/useLoadCommand';
import { useSubmitCall } from './hooks/useSubmitCall';

const useStyles = makeStyles((theme: Theme) => ({
    cardRoot: {
        margin: '2rem 0',
        minWidth: 800
    }
}));
export default function CommandExecutionView() {
    const [response, setResponse] = useState<Object>({});
    const { command, status: commandInfoCallStatus } = useLoadCommand(setResponse);
    const classess = useStyles();
    const isRequiredForm = command?.arguments.length! > 0 || command?.optionalArguments.length! > 0;
    useDirectCall(!isRequiredForm, command?.path, setResponse);
    const { onSubmit } = useSubmitCall(command?.path as string, setResponse);

    if (commandInfoCallStatus !== CallStatus.SUCCESS) {
        return <Typography>Loading...</Typography>;
    }

    if (JSON.stringify(response) !== '{}') {
        return <CommandExecutionResult response={response} />;
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
                    <CommandExecutionForm command={command} onSubmit={onSubmit} setResponse={setResponse} />
                </CardContent>
            </Card>
        );
    }

    return null;
}

import { Card, CardContent, Typography } from '@mui/material';
import { CallStatus } from '../../config';
import CommandExecutionForm from './CommandExecutionForm';
import CommandExecutionResult from './CommandExecutionResult';
import { useDirectCall } from './hooks/useDirectCall';
import { useLoadCommand } from './hooks/useLoadCommand';
import { useSubmitCall } from './hooks/useSubmitCall';

export default function CommandExecutionView() {
    const { command, status } = useLoadCommand();
    const isRequiredForm = command?.arguments.length! > 0 || command?.optionalArguments.length! > 0;
    const { status: directCallStatus, response: directResponse } = useDirectCall(!isRequiredForm, command?.path);
    const { status: formCallStatus, onSubmit, response: formResponse } = useSubmitCall(command?.path as string);

    console.log(isRequiredForm);
    if (formCallStatus === CallStatus.SUCCESS || directCallStatus === CallStatus.SUCCESS) {
        return <CommandExecutionResult response={formResponse || directResponse} />;
    }

    if (isRequiredForm) {
        return (
            <Card sx={{ minWidth: 800 }}>
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

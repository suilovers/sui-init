import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { CallStatus } from '../../../config';
import { fetchCommand } from '../../../services/SuiService';
import { CommandDTO } from '../../../types/sui/response';

export function useLoadCommand() {
    const { childCommand, parentCommand } = useParams();
    const [command, setCommand] = useState<CommandDTO | null>(null);
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);

    useEffect(() => {
        async function loadCommand() {
            try {
                setStatus(CallStatus.LOADING);
                const command = await fetchCommand(parentCommand as string, childCommand as string);
                console.log(command);
                setCommand(command);
                setStatus(CallStatus.SUCCESS);
            } catch (error) {
                setStatus(CallStatus.ERROR);
            }
        }
        if (childCommand && parentCommand) {
            loadCommand();
        }
    }, [childCommand, parentCommand]);

    return { status, command };
}

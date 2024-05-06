import { useEffect, useState } from 'react';
import { CallStatus } from '../../config';
import { getCommandList } from '../../services/SuiService';
import { CommandDTO } from '../../types/sui/response';

export function useLoadCommands() {
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);
    const [commands, setCommands] = useState<CommandDTO[]>([]);

    useEffect(() => {
        async function loadCommands() {
            try {
                setStatus(CallStatus.LOADING);
                const response = await getCommandList();
                setCommands(response);
                setStatus(CallStatus.SUCCESS);
            } catch (error) {
                setStatus(CallStatus.ERROR);
            }
        }

        loadCommands();
    }, []);

    return { status, commands };
}

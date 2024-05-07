import { useEffect, useState } from 'react';
import { CallStatus } from '../../config';
import { fetchCommandList } from '../../services/SuiService';
import { CommandDTO } from '../../types/sui/response';
import { convertCommandMapToList } from '../../utils/command';

export function useLoadCommands() {
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);
    const [commands, setCommands] = useState<CommandDTO[]>([]);

    useEffect(() => {
        async function loadCommands() {
            try {
                setStatus(CallStatus.LOADING);
                const response = await fetchCommandList();
                setCommands(convertCommandMapToList(response));
                setStatus(CallStatus.SUCCESS);
            } catch (error) {
                setStatus(CallStatus.ERROR);
            }
        }

        loadCommands();
    }, []);

    return { status, commands };
}

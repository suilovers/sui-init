import { useState } from 'react';
import { CallStatus } from '../../../config';
import { fetchCall } from '../../../services/SuiService';

export function useSubmitCall(path: string) {
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);
    const [response, setResponse] = useState<any>(null);

    const submitCall = async () => {
        try {
            if (!path) throw new Error('Path is required.');
            setStatus(CallStatus.LOADING);
            const data = await fetchCall(path);
            setResponse(data);
            setStatus(CallStatus.SUCCESS);
        } catch (error) {
            setResponse(error);
            setStatus(CallStatus.ERROR);
        }
    };

    return { status, response, submitCall };
}

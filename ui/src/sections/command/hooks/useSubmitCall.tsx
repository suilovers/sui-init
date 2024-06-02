import { useState } from 'react';
import { CallStatus } from '../../../config';
import { fetchCall } from '../../../services/SuiService';

export function useSubmitCall(path: string, setResponse: (response: Object) => void) {
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        try {
            if (!path) throw new Error('Path is required.');
            setStatus(CallStatus.LOADING);
            const data = await fetchCall(path);
            setResponse(data);
            setStatus(CallStatus.SUCCESS);
        } catch (error) {
            setStatus(CallStatus.ERROR);
        }
    };

    return { status, onSubmit };
}

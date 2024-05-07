import { useEffect, useState } from 'react';
import { CallStatus } from '../../../config';
import { fetchCall } from '../../../services/SuiService';

export function useDirectCall(isDirectCall: boolean, path: string | undefined) {
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);
    const [response, setResponse] = useState<any>(null);

    useEffect(() => {
        async function directCall() {
            try {
                setStatus(CallStatus.LOADING);
                const response = await fetchCall(path as string);
                setResponse(response);
                setStatus(CallStatus.SUCCESS);
            } catch (error) {
                setStatus(CallStatus.ERROR);
            }
        }

        if (isDirectCall && path) {
            directCall();
        }
    }, [isDirectCall, path]);

    return { status, response };
}

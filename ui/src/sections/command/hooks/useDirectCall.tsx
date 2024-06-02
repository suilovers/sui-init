import { useEffect, useState } from 'react';
import { CallStatus } from '../../../config';
import { fetchCall } from '../../../services/SuiService';

export function useDirectCall(isDirectCall: boolean, path: string | undefined, setResponse: (response: Object) => void) {
    const [status, setStatus] = useState<CallStatus>(CallStatus.LOADING);

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
        } else {
            setStatus(CallStatus.LOADING);
        }
    }, [isDirectCall, path, setResponse]);

    return { status };
}

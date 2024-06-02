import { useContext } from 'react';
import { SnackbarContext } from '../contexts/SnackBarContext';

export function useShowSnackbar() {
    const networkContext = useContext(SnackbarContext);
    if (!networkContext) {
        throw new Error('useShowSnackbar must be used within a SnackbarProvider');
    }
    const { showMessage, open, options } = networkContext;

    return {
        showMessage,
        open,
        options
    };
}

import React, { createContext, useEffect, useState } from 'react';

interface SnackbarOptions {
    message: string;
    severity: 'success' | 'error' | 'warning' | 'info';
}

interface SnackbarContextProps {
    options: SnackbarOptions;
    open: boolean;
    showMessage: (options: SnackbarOptions) => void;
}

export const SnackbarContext = createContext<SnackbarContextProps>({
    options: { message: '', severity: 'success' },
    open: false,
    showMessage: () => {}
});

export const SnackbarProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [options, setOptions] = useState<SnackbarOptions>({ message: '', severity: 'success' });
    const [open, setOpen] = useState(false);

    const showMessage = (options: SnackbarOptions) => {
        setOptions(options);
    };

    useEffect(() => {
        if (options.message) {
            setOpen(true);
            setTimeout(() => {
                setOpen(false);
                setOptions({ message: '', severity: 'success' });
            }, 5000);
        }
    }, [options]);
    
    return <SnackbarContext.Provider value={{ options, showMessage, open }}>{children}</SnackbarContext.Provider>;
};

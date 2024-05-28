//create me a modal with mui/material's modal

import React, { ReactNode } from 'react';
import { Box, Modal } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
    modal: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
});

interface ModalProps {
    id?: string;
    children: ReactNode;
    open: boolean;
    onClose: () => void;
}

export default function ModalComponent({ id,children, open, onClose }: ModalProps) {
    const classes = useStyles();
    return (
        <Modal
            id={id}
            open={open}
            onClose={onClose}
            className={classes.modal}
        >
            <Box>
                {children}
            </Box>
        </Modal>
    );
}
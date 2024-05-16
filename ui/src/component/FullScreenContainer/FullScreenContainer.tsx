import { Box } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { ReactNode } from 'react';

const useStyles = makeStyles({
    fullScreenContainer: {
        display: 'flex !important',
        justifyContent: 'center !important',
        alignItems: 'center !important',
        minHeight: 'calc(100vh - 65px)',
        width: 'calc(100vw - 240px)',
        height: 'max-content',
        position: 'relative',
        top: "65px",
        left: '180px'
    }
});

interface FullScreenContainerProps {
    children: ReactNode;
}

export default function FullScreenContainer({ children }: FullScreenContainerProps) {
    const classes = useStyles();
    return <Box className={classes.fullScreenContainer}>{children}</Box>;
}

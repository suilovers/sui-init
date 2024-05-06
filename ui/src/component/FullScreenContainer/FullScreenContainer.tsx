import { Box } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { ReactNode } from 'react';

const useStyles = makeStyles({
    root: {
        display: 'flex !important',
        justifyContent: 'center !important',
        alignItems: 'center !important',
        marginLeft: '240px',
        width: 'calc(100% - 240px)',
        height: '100vh'
    }
});

interface FullScreenContainerProps {
    children: ReactNode;
}

export default function FullScreenContainer({ children }: FullScreenContainerProps) {
    const classes = useStyles();
    return <Box className={classes.root}>{children}</Box>;
}

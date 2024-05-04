import { Container } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { ReactNode } from 'react';

const useStyles = makeStyles({
    root: {
        width: '100vw',
        height: '100vh',
        display: 'flex !important',
        justifyContent: 'center !important',
        alignItems: 'center !important'
    }
});

interface FullScreenContainerProps {
    children: ReactNode;
}

export default function FullScreenContainer({ children }: FullScreenContainerProps) {
    const classes = useStyles();
    return <Container className={classes.root}>{children}</Container>;
}

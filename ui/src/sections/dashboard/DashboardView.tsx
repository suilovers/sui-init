import { Container, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
    root: {
        width: 'calc(100% - 240px)',
        padding: '0px !important',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center'
    },
    welcomeText: {
        margin: '2rem 0',
        textAlign: 'center',
        fontWeight: 'bold',
        fontFamily: 'Roboto, sans-serif'
    }
});
export default function DashboardView() {
    const classes = useStyles();
    return (
        <Container className={classes.root}>
            <Typography variant="h3" className= {classes.welcomeText}>
                Welcome to Sui Initializer!
            </Typography>
        </Container>
    );
}

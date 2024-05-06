import { Container } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
    root: {
        width: '100%',
        padding: '0px !important'
    }
});
export default function DashboardView() {
    const classes = useStyles();
    return <Container className={classes.root}></Container>;
}

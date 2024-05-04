import { Card, CardContent, Grid } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
    card: {
        width: '60%',
        height: '60%'
    }
});
const items = [
    {
        name: 'Pay',
        description: 'Pay for the service'
    },
    {
        name: 'Sui Version',
        description: 'The version of the Sui'
    },
    {
        name: 'Adress',
        description: 'The adress of the service'
    },
    {
        name: 'Envs',
        description: 'The envs of the service'
    },
    {
        name: 'Logs',
        description: 'The logs of the service'
    },
    {
        name: 'Metrics',
        description: 'The metrics of the service'
    },
    {
        name: 'Settings',
        description: 'The settings of the service'
    },
    {
        name: 'Users',
        description: 'The users of the service'
    },
    {
        name: 'Pay',
        description: 'Pay for the service'
    },
    {
        name: 'Sui Version',
        description: 'The version of the Sui'
    },
    {
        name: 'Adress',
        description: 'The adress of the service'
    },
    {
        name: 'Envs',
        description: 'The envs of the service'
    },
    {
        name: 'Logs',
        description: 'The logs of the service'
    },
    {
        name: 'Metrics',
        description: 'The metrics of the service'
    },
    {
        name: 'Settings',
        description: 'The settings of the service'
    },
    {
        name: 'Users',
        description: 'The users of the service'
    }
];

export default function DashboardView() {
    const classes = useStyles();
    return (
        <Card className={classes.card}>
            <CardContent>
                <Grid container spacing={3}>
                    {items.map((box, index) => (
                        <Grid item xs={3} key={index}>
                            <Card>
                                <CardContent>
                                    <h3>{box.name}</h3>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </CardContent>
        </Card>
    );
}

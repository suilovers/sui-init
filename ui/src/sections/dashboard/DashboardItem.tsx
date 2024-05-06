import { Card, CardContent } from '@mui/material';
import { makeStyles } from '@mui/styles';

interface DashboardItemProps {
    name: string;
    description: string;
}

const useStyles = makeStyles({
    card: {
        '&:hover': {
            transform: 'scale(1.02)', // Change this to your liking
            boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)' // Change this to your liking
        },
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out'
    }
});

export default function DashboardItem({ name, description }: DashboardItemProps) {
    const classes = useStyles();
    return (
        <Card className={classes.card}>
            <CardContent>
                <h3>{name}</h3>
                <p>{description}</p>
            </CardContent>
        </Card>
    );
}

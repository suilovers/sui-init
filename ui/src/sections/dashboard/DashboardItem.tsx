import { Card, CardContent } from '@mui/material';

interface DashboardItemProps {
    name: string;
    description: string;
}
export default function DashboardItem({ name, description }: DashboardItemProps) {
    return (
        <Card>
            <CardContent>
                <h3>{name}</h3>
                <p>{description}</p>
            </CardContent>
        </Card>
    );
}

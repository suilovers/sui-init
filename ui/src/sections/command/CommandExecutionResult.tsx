import { Card, CardContent, Theme } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { Graph } from 'jsoncrack-react';
import { useCopyNode } from './hooks/useCopyNode';

interface CommandExecutionResultProps {
    response: any;
}

const useStyles = makeStyles((theme: Theme) => ({
    cardRoot: {
        margin: '2rem 0',
        padding: theme.spacing(2),
        boxSizing: 'border-box'
    }
}));
export default function CommandExecutionResult({ response }: CommandExecutionResultProps) {
    const classess = useStyles();
    const { onNodeClick } = useCopyNode();
    return (
        <Card className={classess.cardRoot}>
            <CardContent>
                <Graph onNodeClick={onNodeClick} json={JSON.stringify(response)} />
            </CardContent>
        </Card>
    );
}

import { Card, CardContent, Theme } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { JsonViewer } from '@textea/json-viewer';
import { useExecutionResult } from './hooks/useExecutionResult';

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
    const { addressDataType, stringArrayDataType, objectArrayDataType } = useExecutionResult();
    return (
        <Card className={classess.cardRoot}>
            <CardContent>
                <JsonViewer rootName={false} theme="dark" value={response} valueTypes={[addressDataType, stringArrayDataType, objectArrayDataType]} />
            </CardContent>
        </Card>
    );
}

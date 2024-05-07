import { JsonViewer } from '@textea/json-viewer';

interface CommandExecutionResultProps {
    response: any;
}
export default function CommandExecutionResult({ response }: CommandExecutionResultProps) {
    return <JsonViewer theme="dark" value={response} />;
}

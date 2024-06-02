import { useShowSnackbar } from '../../../hooks/useToggleSnackbar';

declare type NodeType = 'object' | 'array' | 'property' | 'string' | 'number' | 'boolean' | 'null';

interface NodeData {
    id: string;
    text: string | [string, string][];
    width: number;
    height: number;
    path?: string;
    data: {
        type: NodeType;
        isParent: boolean;
        isEmpty: boolean;
        childrenCount: number;
    };
}
export function useCopyNode() {
    const { showMessage } = useShowSnackbar();
    async function onNodeClick(node: NodeData) {
        let jsonString = '';
        if (Array.isArray(node.text)) {
            const obj = Object.fromEntries(node.text as [string, string][]);

            // Convert the object to a JSON string
            jsonString = JSON.stringify(obj, null, 2);
        } else {
            jsonString = node.text as string;
        }

        // Copy the JSON string to the clipboard
        await navigator.clipboard.writeText(jsonString);

        console.log('Node copied to clipboard');
        // Show a snackbar message
        showMessage({
            message: 'Node copied to clipboard',
            severity: 'success'
        });
    }
    return { onNodeClick };
}

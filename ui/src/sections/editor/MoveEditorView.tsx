import { Editor } from '@monaco-editor/react';

export default function MoveEditorView() {
    // const monaco = useMonaco() as Monaco | null;

    // useEffect(() => {
    //     if (monaco) {
    //         console.log('here is the monaco instance:', monaco);
    //         console.log(monaco.languages);
    //     }
    // }, [monaco]);

    return <Editor height="calc(100vh - 64px)" theme="vs-dark" defaultLanguage="javascript" defaultValue="// some comment" />;
}

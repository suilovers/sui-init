import { useRef } from 'react';
import { Monaco } from '@monaco-editor/react';

const useMonacoSetup = () => {
    const monacoRef = useRef(null);
    const editorRef = useRef<Monaco | null>(null);

    const handleEditorWillMount = (monaco: any) => {
        monaco.languages.register({ id: 'move' });

        monaco.languages.setMonarchTokensProvider('move', {
            tokenizer: {
                root: [
                    [/[{}()\[\]]/, 'delimiter.bracket'],
                    [/[,:;]/, 'delimiter'],
                    [/[a-zA-Z_]\w*/, {
                        cases: {
                            '@keywords': 'keyword',
                            '@builtinTypes': 'type',
                            '@default': 'variable'
                        }
                    }],
                    { include: '@whitespace' },
                    [/[ \t\r\n]+/, ''],
                    [/\/\*/, 'comment', '@comment'],
                    [/\/\/.*$/, 'comment'],
                    [/"([^"\\]|\\.)*$/, 'string.invalid'],
                    [/"/, 'string', '@string'],
                    [/\d+/, 'number'],
                    [/[+\-*/%=!<>&|]/, 'operator']
                ],

                comment: [
                    [/[^\/*]+/, 'comment'],
                    [/\*\//, 'comment', '@pop'],
                    [/[\/*]/, 'comment']
                ],

                string: [
                    [/[^\\"]+/, 'string'],
                    [/\\./, 'string.escape'],
                    [/"/, 'string', '@pop']
                ],

                whitespace: [
                    [/[ \t\r\n]+/, '']
                ],
            },

            keywords: [
                'module', 'script', 'fun', 'struct', 'public', 'resource',
                'move', 'copy', 'use', 'address', 'main', 'has', 'acquires',
                'let', 'if', 'else', 'while', 'return', 'abort', 'true',
                'false', 'break', 'continue', 'as', 'mut', 'borrow', 'spec',
                'native', 'const', 'module'
            ],

            builtinTypes: [
                'bool', 'u8', 'u64', 'u128', 'address', 'vector'
            ],

            operators: [
                '=', '==', '!=', '<', '<=', '>', '>=', '+', '-', '*', '/', '%',
                '!', '&&', '||', '->', '<-'
            ]
        });

        monaco.editor.defineTheme('moveTheme', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: 'keyword', foreground: '00BFFF', fontStyle: 'bold' },
                { token: 'type', foreground: '00ff00' },
                { token: 'variable', foreground: 'FFA500' },
                { token: 'delimiter', foreground: 'ff00ff' },
                { token: 'delimiter.bracket', foreground: 'ffff00' },
                { token: 'comment', foreground: '808080', fontStyle: 'italic' },
                { token: 'string', foreground: 'D8BFD8' },
                { token: 'number', foreground: '00ffff' },
                { token: 'operator', foreground: 'ffffff' }
            ],
            colors: {
                'editor.foreground': '#F8F8F8',
                'editor.background': '#1E1E1E',
                'editorCursor.foreground': '#A7A7A7',
                'editor.lineHighlightBackground': '#333333',
                'editorLineNumber.foreground': '#858585',
                'editor.selectionBackground': '#264F78',
                'editor.inactiveSelectionBackground': '#3A3D41'
            }
        });

        monaco.languages.registerCompletionItemProvider('move', {
            provideCompletionItems: function (model: any, position: any) {
                const keywords = [
                    'module', 'script', 'fun', 'struct', 'public', 'resource',
                    'move', 'copy', 'use', 'address', 'main', 'has', 'acquires',
                    'let', 'if', 'else', 'while', 'return', 'abort', 'true',
                    'false', 'break', 'continue', 'as', 'mut', 'borrow', 'spec',
                    'native', 'const', 'module'
                ];

                const suggestions = keywords.map(keyword => ({
                    label: keyword,
                    kind: monaco.languages.CompletionItemKind.Keyword,
                    insertText: keyword
                }));

                return { suggestions: suggestions };
            }
        });
    };

    const handleEditorDidMount = (editor: any, monaco: any) => {
        monacoRef.current = monaco;
        editorRef.current = editor;

        monaco.languages.setLanguageConfiguration('move', {
            autoClosingPairs: [
                { open: '{', close: '}' },
                { open: '[', close: ']' },
                { open: '(', close: ')' },
                { open: '"', close: '"' },
                { open: "'", close: "'" }
            ]
        });
    };

    return {
        handleEditorWillMount,
        handleEditorDidMount,
        monacoRef,
        editorRef
    };
};

export default useMonacoSetup;

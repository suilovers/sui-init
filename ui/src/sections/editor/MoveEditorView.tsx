import React, { useEffect, useRef, useState } from 'react';
import Editor, { Monaco } from '@monaco-editor/react';
import ModalComponent from '../../component/Modal';
import MoveMenuButton from './MoveMenuButton';
import { fetchCallWithBody } from '../../services/SuiService';

export default function MoveEditorView() {
    type SourceTestType = Record<string, string>; // replace string with the correct type if necessary

    const [open, setOpen] = useState(false);
    const [children, setChildren] = useState<any>(null);
    const [projectName, setProjectName] = useState('');
    const [click , setClick] = useState('');
    const [sources, setSources] = useState<SourceTestType>({
        "deneme1.move": "// filename: sources/my_module.move\r\nmodule 0x1::my_module {\r\n\r\n    struct MyCoin has key { value: u64 }\r\n\r\n    public fun make_sure_non_zero_coin(coin: MyCoin): MyCoin {\r\n        assert!(coin.value > 0, 0);\r\n        coin\r\n    }\r\n\r\n    public fun has_coin(addr: address): bool {\r\n        exists<MyCoin>(addr)\r\n    }\r\n\r\n    #[test]\r\n    fun make_sure_non_zero_coin_passes() {\r\n        let coin = MyCoin { value: 1 };\r\n        let MyCoin { value: _ } = make_sure_non_zero_coin(coin);\r\n    }\r\n\r\n    #[test]\r\n    // Or #[expected_failure] if we don't care about the abort code\r\n    #[expected_failure(abort_code = 0)]\r\n    fun make_sure_zero_coin_fails() {\r\n        let coin = MyCoin { value: 0 };\r\n        let MyCoin { value: _ } = make_sure_non_zero_coin(coin);\r\n    }\r\n\r\n    #[test_only] // test only helper function\r\n    fun publish_coin(account: &signer) {\r\n        move_to(account, MyCoin { value: 1 })\r\n    }\r\n\r\n    #[test(a = @0x1, b = @0x2)]\r\n    fun test_has_coin(a: signer, b: signer) {\r\n        publish_coin(&a);\r\n        publish_coin(&b);\r\n        assert!(has_coin(@0x1), 0);\r\n        assert!(has_coin(@0x2), 1);\r\n        assert!(!has_coin(@0x3), 1);\r\n    }\r\n}",
        "deneme2.move": "dssdsd"
    });
    const [tests, setTests] = useState<SourceTestType>({});
    const [toml, setToml] = useState('');

    useEffect(() => {
        if(click === "Create"){
            console.log(projectName);
            fetchCallWithBody('/move/create', {projectName: projectName})
                .then(response => {
                    setSources(response.sources);
                    setTests(response.tests);
                    setToml(response.toml);
                });
            setClick('');
        }
        else if(click === "Open"){
            console.log(projectName);
            fetchCallWithBody('/move/open', {projectName: projectName})
                .then(response => {
                    setSources(response.sources);
                    setTests(response.tests);
                    setToml(response.toml);
                });
            setClick('');
        }
    }, [click]);

    function changeInput(e: React.ChangeEvent<HTMLInputElement>) {
        setProjectName(e.target.value);
    }

    function handleOpen() {
        setOpen(!open);
    }

    function changeChildren(newChildren: any) {
        setChildren(newChildren);
    }
    const monacoRef = useRef(null);

    const editorRef = useRef<Monaco | null>(null);

    function buttonClick(funcName: string) {
        setClick(funcName);
    }

    function handleEditorWillMount(monaco: any) {
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
    }

    function handleEditorDidMount(editor: any, monaco: any) {
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
    }

    return (
        <div style={{ display: 'flex', height: '100vh', width: '200vh' }}>
        <div id='main' style={{ flex: 1 }}>
            <ModalComponent id="moveModal" children={children} open={open} onClose={handleOpen} />
            
            <Editor
                beforeMount={handleEditorWillMount}
                onMount={handleEditorDidMount}
                theme="moveTheme"
                defaultLanguage="move"
                defaultValue={`module MyModule {
use 0x1::Coin;
use 0x1::Signer;

struct MyStruct has copy, drop {
    value: u64,
}

public fun my_function(account: &signer) {
    let x = 10;
    let y = 20;
    let result = x + y;
    let my_struct = MyStruct { value: result };
    Coin::deposit(account, my_struct.value);
    return my_struct;
}

public fun another_function() {
    let condition = true;
    if (condition) {
        return 1;
    } else {
        return 0;
    }
}
}`}
            />
        </div>
        <div style={{ width: '300px', backgroundColor: '#2e2e2e', padding: '10px', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center' }}>
            <MoveMenuButton changeInput={changeInput} buttonText="Create New Move Project" buttonLabel="Create" placeholder="Enter the Project Name" run={handleOpen} changeChildren={changeChildren} formRun={() => buttonClick("Create")}/>
            <MoveMenuButton changeInput={changeInput} buttonText='Open Existing Move Project' buttonLabel='Open' placeholder='Enter the Project Name' run={handleOpen} changeChildren={changeChildren} formRun={() => buttonClick("Open")}/>
            <div style={{ marginBottom: '10px' }}>
                <h3>Sources</h3>
                {Object.keys(sources).map(filename => (
                    <div key={filename}>
                        <button onClick={() => editorRef.current.setValue(sources[filename])}>{filename}</button>
                    </div>
                ))}
            </div>
            <div style={{ marginBottom: '10px' }}>
                <h3>Tests</h3>
                {Object.keys(tests).map(filename => (
                    <div key={filename}>
                        <button onClick={() => editorRef.current.setValue(tests[filename])}>{filename}</button>
                    </div>
                ))}
            </div>
            <div style={{ marginBottom: '10px' }}>
                <h3>TOML</h3>
            </div>
        </div>
    </div>

    );
}


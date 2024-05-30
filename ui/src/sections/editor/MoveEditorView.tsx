import React, { useEffect } from 'react';
import Editor from '@monaco-editor/react';
import ModalComponent from '../../component/Modal';
import MoveMenuButton from './MoveMenuButton';
import { Box, Button, List, ListItem, ListItemText } from '@mui/material';
import useProjectManager from './hooks/useProjectManager';
import useMonacoSetup from './hooks/useMonacoSetup';
import { initialValue } from './initialValue';

export default function MoveEditorView() {
    const {
        open,
        children,
        projectName,
        sources,
        tests,
        toml,
        currentFile,
        setClick,
        changeInput,
        handleOpen,
        changeChildren,
        saveProject,
        setCurrentFile
    } = useProjectManager();

    const {
        handleEditorWillMount,
        handleEditorDidMount,
        monacoRef,
        editorRef
    } = useMonacoSetup();

    // on editorRef change, set the value of the editor to the current file content
    useEffect(() => {
        if (editorRef.current && currentFile.content) {
            editorRef.current.setValue(currentFile.content);
        }
    }, [editorRef, currentFile]);
    
    return (
        <div style={{ display: 'flex', height: '100vh', width: '200vh' }}>
            <div id='main' style={{ flex: 1 }}>
                <ModalComponent id="moveModal" children={children} open={open} onClose={handleOpen} />
                <Editor
                    beforeMount={handleEditorWillMount}
                    onMount={handleEditorDidMount}
                    theme="moveTheme"
                    defaultLanguage="move"
                    defaultValue={initialValue}
                />
            </div>
            <div style={{ width: '300px', backgroundColor: '#2e2e2e', padding: '10px', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center' }}>
                <MoveMenuButton changeInput={changeInput} buttonText="Create New Move Project" buttonLabel="Create" placeholder="Enter the Project Name" run={handleOpen} changeChildren={changeChildren} formRun={() => setClick("Create")} />
                <MoveMenuButton changeInput={changeInput} buttonText='Open Existing Move Project' buttonLabel='Open' placeholder='Enter the Project Name' run={handleOpen} changeChildren={changeChildren} formRun={() => setClick("Open")} />
                <Box mb={2}>
                    <List>
                        <ListItem>
                            <ListItemText primary="Sources" style={{ textAlign: 'center' }} />
                        </ListItem>
                        {Object.keys(sources).map(filename => (
                            <ListItem key={filename}>
                                <Button variant="contained" color="primary" onClick={() => {editorRef.current.setValue(sources[filename])
                                    setCurrentFile({ filename, type: 'source', content: sources[filename] })
                                }}>
                                    {filename}
                                </Button>
                            </ListItem>
                        ))}
                    </List>
                </Box>
                <Box mb={2}>
                    <List>
                        <ListItem>
                            <ListItemText primary="Tests" style={{ textAlign: 'center' }} />
                        </ListItem>
                        {Object.keys(tests).map(filename => (
                            <ListItem key={filename}>
                                <Button variant="contained" color="primary" onClick={() => {editorRef.current.setValue(tests[filename])
                                    setCurrentFile({ filename, type: 'test', content: tests[filename] })
                                }}>
                                    {filename}
                                </Button>
                            </ListItem>
                        ))}
                    </List>
                </Box>
                <Box mb={2}>
                    <List>
                        <ListItem>
                            <ListItemText primary="TOML" style={{ textAlign: 'center' }} />
                        </ListItem>
                    </List>
                </Box>
                <Button variant="contained" color="primary" onClick={saveProject}>Save All Project</Button>
            </div>
        </div>
    );
}

import Editor from '@monaco-editor/react';
import FolderIcon from '@mui/icons-material/Folder';
import { Avatar, Box, Button, Divider, List, ListItem, ListItemAvatar, ListItemText, Typography } from '@mui/material';
import { useEffect } from 'react';
import ModalComponent from '../../component/Modal';
import { CallStatus } from '../../config';
import MoveEditorProjectStructureTree from './MoveEditorProjectStructureTree';
import MoveEditorResponseGraphModal from './MoveEditorResponseGraphModal';
import MoveMenuButton from './MoveMenuButton';
import useMonacoSetup from './hooks/useMonacoSetup';
import useProjectManager from './hooks/useProjectManager';
import { initialValue } from './initialValue';

export default function MoveEditorView() {
    const { handleEditorWillMount, handleEditorDidMount, editorRef } = useMonacoSetup();
    const {
        open,
        children,
        sources,
        tests,
        toml,
        currentFile,
        projects,
        projectName,
        writingStatus,
        response,
        setClick,
        setProjectNameInput,
        handleOpen,
        changeChildren,
        setCurrentFile,
        changeFileName,
        buildProject,
        testProject,
        deleteProject,
        publishProject,
        openProject,
        handleDelayedWritingStatusUpdate,
        handleAutoUpdate,
        setResponse
    } = useProjectManager();

    useEffect(() => {
        if (editorRef.current && currentFile && writingStatus === CallStatus.SUCCESS) {
            const content = editorRef.current.getValue();
            const file = editorRef.current.file;
            handleAutoUpdate(file, content);
        }
    }, [currentFile, editorRef, writingStatus]);

    return (
        <div style={{ display: 'flex', height: '150vh', width: '100vw' }}>
            <div id="main" style={{ flex: 1 }}>
                <MoveEditorResponseGraphModal response={response} onClose={() => setResponse({})} />
                <ModalComponent id="moveModal" children={children} open={open} onClose={handleOpen} />
                <Editor
                    beforeMount={handleEditorWillMount}
                    onMount={handleEditorDidMount}
                    theme="moveTheme"
                    defaultLanguage="move"
                    defaultValue={initialValue}
                    onChange={() => handleDelayedWritingStatusUpdate()}
                />
            </div>
            <div
                style={{
                    backgroundColor: '#2e2e2e',
                    padding: '10px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'flex-start',
                    alignItems: 'center'
                }}
            >
                <MoveMenuButton
                    changeInput={(e) => setProjectNameInput(e.target.value)}
                    buttonText="Create New Move Project"
                    buttonLabel="Create"
                    placeholder="Enter the Project Name"
                    run={handleOpen}
                    changeChildren={changeChildren}
                    formRun={() => setClick('Create')}
                />
                {projectName && (
                    <>
                        <MoveMenuButton
                            changeInput={changeFileName}
                            buttonText="Create Source File"
                            buttonLabel="Create"
                            placeholder="Enter the File Name"
                            run={handleOpen}
                            changeChildren={changeChildren}
                            formRun={() => setClick('Source')}
                        />
                        <MoveMenuButton
                            changeInput={changeFileName}
                            buttonText="Create Test File"
                            buttonLabel="Create"
                            placeholder="Enter the File Name"
                            run={handleOpen}
                            changeChildren={changeChildren}
                            formRun={() => setClick('Test')}
                        />
                        <MoveMenuButton
                            changeInput={changeFileName}
                            buttonText="Delete Source File"
                            buttonLabel="Delete"
                            placeholder="Enter the File Name"
                            run={handleOpen}
                            changeChildren={changeChildren}
                            formRun={() => setClick('DeleteSource')}
                        />
                        <MoveMenuButton
                            changeInput={changeFileName}
                            buttonText="Delete Test File"
                            buttonLabel="Delete"
                            placeholder="Enter the File Name"
                            run={handleOpen}
                            changeChildren={changeChildren}
                            formRun={() => setClick('DeleteTest')}
                        />
                    </>
                )}

                {projectName && (
                    <MoveEditorProjectStructureTree
                        editorRef={editorRef}
                        sources={sources}
                        tests={tests}
                        toml={toml}
                        setCurrentFile={setCurrentFile}
                    />
                )}

                {projectName && (
                    <>
                        <Button variant="contained" color="primary" style={{ marginBottom: '10px' }} onClick={buildProject}>
                            Build Project
                        </Button>
                        <Button variant="contained" color="primary" style={{ marginBottom: '10px' }} onClick={testProject}>
                            Test Project
                        </Button>
                        <Button variant="contained" color="primary" style={{ marginBottom: '10px' }} onClick={deleteProject}>
                            Delete Project
                        </Button>
                        <Button variant="contained" color="primary" style={{ marginBottom: '10px' }} onClick={publishProject}>
                            Publish Project
                        </Button>
                    </>
                )}

                <Box
                    my={2}
                    sx={{
                        width: '100%',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center'
                    }}
                >
                    <Typography
                        variant="h6"
                        style={{
                            color: 'white',
                            marginBottom: '10px'
                        }}
                    >
                        Projects
                    </Typography>
                    <Divider
                        style={{
                            width: '100%'
                        }}
                    />
                    <List>
                        {projects.map((project) => (
                            <ListItem key={project.projectName} onClick={() => openProject(project.projectName)} style={{ cursor: 'pointer' }}>
                                <ListItemAvatar>
                                    <Avatar>
                                        <FolderIcon
                                            sx={{
                                                color: 'white'
                                            }}
                                        />
                                    </Avatar>
                                </ListItemAvatar>
                                <ListItemText primary={project.projectName} secondary={project.lastUpdated} />
                            </ListItem>
                        ))}
                        <ListItem></ListItem>
                    </List>
                </Box>
            </div>
        </div>
    );
}

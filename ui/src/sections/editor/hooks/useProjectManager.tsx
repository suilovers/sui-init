import { useEffect, useState } from 'react';
import { CallStatus } from '../../../config';
import { useShowSnackbar } from '../../../hooks/useToggleSnackbar';
import { fetchCallWithBody } from '../../../services/SuiService';
import { sleep } from '../../../utils/time';

type SourceTestType = Record<string, string>;

interface ProjectInfo {
    projectName: string;
    lastUpdated: string;
}
interface CurrentFile {
    fileName: string;
    type: string;
    content: string;
}

const useProjectManager = () => {
    const [response, setResponse] = useState<Object>({});
    const { showMessage } = useShowSnackbar();
    const [writingStatus, setWritingStatus] = useState<CallStatus>(CallStatus.SUCCESS);
    const [open, setOpen] = useState(false);
    const [children, setChildren] = useState<any>(null);
    const [projectName, setProjectName] = useState<string | null>(null);
    const [projectNameInput, setProjectNameInput] = useState<string>('');
    const [click, setClick] = useState('');
    const [sources, setSources] = useState<SourceTestType>({});
    const [tests, setTests] = useState<SourceTestType>({});
    const [toml, setToml] = useState('');
    const [currentFile, setCurrentFile] = useState<CurrentFile>({ fileName: '', type: '', content: '' });
    const [createdFileName, setCreatedFileName] = useState('');
    const [projects, setProjects] = useState<ProjectInfo[]>([]);
    let timeoutId: NodeJS.Timeout | null = null;
    async function fetchProjects() {
        const response = await fetchCallWithBody('/move/list', {});
        const projects = response.projects.map((project: any) => {
            return {
                projectName: project['name'] as string,
                lastUpdated: project['last_updated']
            };
        });
        setProjects(projects);
    }
    useEffect(() => {
        fetchProjects();
    }, []);

    async function handleAutoUpdate(currentFile: CurrentFile, text: string) {
        if (!projectName || !currentFile || !currentFile.fileName) return;
        const file = { ...currentFile, content: text };
        setCurrentFile(file);
        updateFileStates(file);
        try {
            await fetchCallWithBody('/move/update', {
                projectName,
                fileName: file.fileName,
                fileContent: file.content
            });
        } catch (error) {
            console.error(error);
        }
        setWritingStatus(CallStatus.LOADING);
    }

    const handleDelayedWritingStatusUpdate = () => {
        setWritingStatus(CallStatus.LOADING);
        if (timeoutId) {
            clearTimeout(timeoutId);
        }

        timeoutId = setTimeout(() => {
            setWritingStatus(CallStatus.SUCCESS);
        }, 1500); // 1 second delay
    };

    async function openProject(projectName: string) {
        try {
            const response = await fetchCallWithBody('/move/open', { projectName });
            setProjectName(projectName);
            setSources(response.sources);
            setTests(response.tests);
            setToml(response.toml);
        } catch (error) {
            console.error(error);
        }
    }

    function updateFileStates(currentFile: CurrentFile) {
        if (currentFile.type === 'source') {
            setSources((sources) => ({ ...sources, [currentFile.fileName]: currentFile.content }));
        } else if (currentFile.type === 'test') {
            setTests((tests) => ({ ...tests, [currentFile.fileName]: currentFile.content }));
        } else if (currentFile.type === 'toml') {
            setToml(currentFile.content);
        }
    }

    async function createProject() {
        if (!projectNameInput) return;
        const response = await fetchCallWithBody('/move/create', { projectName: projectNameInput });
        setSources(response.sources);
        setTests(response.tests);
        setToml(response.toml);
        await fetchProjects();
        openProject(projectName as string);
    }

    useEffect(() => {
        if (click === 'Create') {
            createProject();
        } else if (click === 'Source') {
            setSources({ ...sources, [createdFileName + '.move']: '' });
            setCurrentFile({ fileName: createdFileName + '.move', type: 'source', content: '' });
        } else if (click === 'Test') {
            setTests({ ...tests, [createdFileName + '.move']: '' });
            setCurrentFile({ fileName: createdFileName + '.move', type: 'test', content: '' });
        } else if (click === 'DeleteSource') {
            const newSources = { ...sources };
            delete newSources[createdFileName + '.move'];
            setCurrentFile({ fileName: '', type: '', content: '' });
            setSources(newSources);
        } else if (click === 'DeleteTest') {
            const newTests = { ...tests };
            delete newTests[createdFileName + '.move'];
            setCurrentFile({ fileName: '', type: '', content: '' });
            setTests(newTests);
        }
        if (open) {
            handleOpen();
        }
        setClick('');
    }, [click, projectName]);

    const changeFileName = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCreatedFileName(e.target.value);
    };

    const handleOpen = () => {
        setOpen(!open);
    };

    const changeChildren = (newChildren: any) => {
        setChildren(newChildren);
    };

    async function buildProject() {
        showMessage({
            message: 'Building project...',
            severity: 'info'
        });
        const response = await fetchCallWithBody('/move/build', { projectName });
        await sleep(5000);
        if (response.output && response.output.includes('error')) {
            showMessage({
                message: response.output,
                severity: 'error'
            });
            return;
        } else {
            showMessage({
                message: 'Project built successfully!',
                severity: 'success'
            });
        }
    }

    async function testProject() {
        showMessage({
            message: 'Testing project...',
            severity: 'info'
        });
        const response = await fetchCallWithBody('/move/test', { projectName });
        await sleep(5000);
        if (response.output && response.output.includes('error')) {
            showMessage({
                message: response.output,
                severity: 'error'
            });
            return;
        } else {
            showMessage({
                message: 'Project tested successfully!',
                severity: 'success'
            });
        }
    }

    const deleteProject = () => {
        fetchCallWithBody('/move/delete', { projectName });
        setSources({});
        setTests({});
        setToml('');
        setCurrentFile({ fileName: '', type: '', content: '' });
    };

    async function publishProject() {
        showMessage({
            message: 'Testing project...',
            severity: 'info'
        });
        const response = await fetchCallWithBody('/move/publish', { projectName, budget: '10000000' });
        await sleep(5000);
        if (response && response.includes('error')) {
            showMessage({
                message: response,
                severity: 'error'
            });
            return;
        } else {
            showMessage({
                message: 'Project tested successfully!',
                severity: 'success'
            });
            setResponse(response);
        }
    }

    return {
        open,
        children,
        projectName,
        sources,
        tests,
        toml,
        currentFile,
        projects,
        writingStatus,
        response,
        setClick,
        handleOpen,
        changeChildren,
        setCurrentFile,
        setProjectNameInput,
        changeFileName,
        buildProject,
        testProject,
        deleteProject,
        publishProject,
        openProject,
        handleDelayedWritingStatusUpdate,
        setWritingStatus,
        handleAutoUpdate,
        setResponse
    };
};

export default useProjectManager;

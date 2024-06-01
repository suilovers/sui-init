import { useState, useEffect } from 'react';
import { fetchCallWithBody } from '../../../services/SuiService';

type SourceTestType = Record<string, string>;

const useProjectManager = () => {
    const [open, setOpen] = useState(false);
    const [children, setChildren] = useState<any>(null);
    const [projectName, setProjectName] = useState('');
    const [click, setClick] = useState('');
    const [sources, setSources] = useState<SourceTestType>({});
    const [tests, setTests] = useState<SourceTestType>({});
    const [toml, setToml] = useState('');
    const [currentFile, setCurrentFile] = useState({ filename: '',type:'', content: '' });
    const [createdFileName, setCreatedFileName] = useState('');

    useEffect(() => {
        if (click === "Create") {
            fetchCallWithBody('/move/create', { projectName })
                .then(response => {
                    setSources(response.sources);
                    setTests(response.tests);
                    setToml(response.toml);
                });
            setClick('');
        } else if (click === "Open") {
            fetchCallWithBody('/move/open', { projectName })
                .then(response => {
                    setSources(response.sources);
                    setTests(response.tests);
                    console.log(response.toml);
                    setToml(response.toml);
                });
            setClick('');
        } else if (click === "Source") {
            setCurrentFile({ filename: createdFileName+".move", type: 'source', content: '' });
            console.log(sources);
            setClick('');
        } else if (click === "Test") {
            setCurrentFile({ filename: createdFileName+".move", type: 'test', content: '' });
            setClick('');
        } else if (click === "DeleteSource") {
            const newSources = { ...sources };
            delete newSources[createdFileName+".move"];
            // set current file to empty
            setCurrentFile({ filename: '', type: '', content: '' });
            setSources(newSources);
            setClick('');
        } else if (click === "DeleteTest") {
            const newTests = { ...tests };
            delete newTests[createdFileName+".move"];
            setCurrentFile({ filename: '', type: '', content: '' });
            setTests(newTests);
            setClick('');
        }
    }, [click, projectName]);

    const changeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        setProjectName(e.target.value);
    };

    const changeFileName = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCreatedFileName(e.target.value);
    }

    const handleOpen = () => {
        setOpen(!open);
    };

    const changeChildren = (newChildren: any) => {
        setChildren(newChildren);
    };

    const saveProject = () => {
        fetchCallWithBody('/move/save', { projectName, sources, tests, toml });
    };

    const buildProject = () => {
        fetchCallWithBody('/move/build', { projectName });
    };

    const testProject = () => {
        fetchCallWithBody('/move/test', { projectName });
    }
    const deleteProject = () => {
        fetchCallWithBody('/move/delete', { projectName });
        setSources({});
        setTests({});
        setToml('');
        setCurrentFile({ filename: '', type: '', content: '' });
    }

    return {
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
        setCurrentFile,
        setSources,
        setTests,
        setToml,
        changeFileName,
        buildProject,
        testProject,
        deleteProject
    };
};

export default useProjectManager;

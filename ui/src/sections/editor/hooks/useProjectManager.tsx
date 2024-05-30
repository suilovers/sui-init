import { useState, useEffect } from 'react';
import { fetchCallWithBody } from '../../../services/SuiService';

type SourceTestType = Record<string, string>;

const useProjectManager = () => {
    const [open, setOpen] = useState(false);
    const [children, setChildren] = useState<any>(null);
    const [projectName, setProjectName] = useState('');
    const [click, setClick] = useState('');
    const [sources, setSources] = useState<SourceTestType>({
        "deneme1.move": "// filename: sources/my_module.move\r\nmodule 0x1::my_module {\r\n\r\n    struct MyCoin has key { value: u64 }\r\n\r\n    public fun make_sure_non_zero_coin(coin: MyCoin): MyCoin {\r\n        assert!(coin.value > 0, 0);\r\n        coin\r\n    }\r\n\r\n    public fun has_coin(addr: address): bool {\r\n        exists<MyCoin>(addr)\r\n    }\r\n\r\n    #[test]\r\n    fun make_sure_non_zero_coin_passes() {\r\n        let coin = MyCoin { value: 1 };\r\n        let MyCoin { value: _ } = make_sure_non_zero_coin(coin);\r\n    }\r\n\r\n    #[test]\r\n    // Or #[expected_failure] if we don't care about the abort code\r\n    #[expected_failure(abort_code = 0)]\r\n    fun make_sure_zero_coin_fails() {\r\n        let coin = MyCoin { value: 0 };\r\n        let MyCoin { value: _ } = make_sure_non_zero_coin(coin);\r\n    }\r\n\r\n    #[test_only] // test only helper function\r\n    fun publish_coin(account: &signer) {\r\n        move_to(account, MyCoin { value: 1 })\r\n    }\r\n\r\n    #[test(a = @0x1, b = @0x2)]\r\n    fun test_has_coin(a: signer, b: signer) {\r\n        publish_coin(&a);\r\n        publish_coin(&b);\r\n        assert!(has_coin(@0x1), 0);\r\n        assert!(has_coin(@0x2), 1);\r\n        assert!(!has_coin(@0x3), 1);\r\n    }\r\n}",
        "deneme2.move": "dssdsd"
    });
    const [tests, setTests] = useState<SourceTestType>({});
    const [toml, setToml] = useState('');
    const [currentFile, setCurrentFile] = useState({ filename: '',type:'', content: '' });

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
                    setToml(response.toml);
                });
            setClick('');
        }
    }, [click, projectName]);

    const changeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        setProjectName(e.target.value);
    };

    const handleOpen = () => {
        setOpen(!open);
    };

    const changeChildren = (newChildren: any) => {
        setChildren(newChildren);
    };

    const saveProject = () => {
        fetchCallWithBody('/move/save', { projectName, sources, tests, toml });
    };

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
        setCurrentFile
    };
};

export default useProjectManager;

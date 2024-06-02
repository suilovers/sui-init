import FolderIcon from '@mui/icons-material/Folder';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { Box, Typography } from '@mui/material';
import { SimpleTreeView, TreeItem } from '@mui/x-tree-view';
interface MoveEditorProjectStructureTreeProps {
    editorRef: any;
    sources: any;
    tests: any;
    toml: string;
    setCurrentFile: any;
}
export default function MoveEditorProjectStructureTree({ editorRef, sources, tests, toml, setCurrentFile }: MoveEditorProjectStructureTreeProps) {
    return (
        <Box mb={2}>
            <Typography variant="h6" style={{ color: 'white', marginBottom: '10px' }}>
                Project Files
            </Typography>
            <SimpleTreeView defaultExpandedItems={['1', '2']}>
                <TreeItem
                    itemId="1"
                    label={
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center'
                            }}
                        >
                            <FolderIcon
                                sx={{
                                    mr: 1
                                }}
                            />
                            <Typography style={{ color: 'white' }}>src</Typography>
                        </Box>
                    }
                >
                    {Object.keys(sources).map((fileName) => (
                        <TreeItem
                            key={fileName}
                            itemId={fileName}
                            label={
                                <Box
                                    sx={{
                                        display: 'flex',
                                        alignItems: 'center'
                                    }}
                                >
                                    <InsertDriveFileIcon
                                        sx={{
                                            mr: 1
                                        }}
                                    />
                                    <Typography style={{ color: 'white' }}>{fileName}</Typography>
                                </Box>
                            }
                            onClick={() => {
                                editorRef.current.setValue(sources[fileName]);
                                editorRef.current.file = {
                                    fileName,
                                    type: 'source'
                                };
                                setCurrentFile({
                                    fileName,
                                    type: 'source',
                                    content: sources[fileName]
                                });
                            }}
                        />
                    ))}
                </TreeItem>

                <TreeItem
                    itemId="2"
                    label={
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center'
                            }}
                        >
                            <FolderIcon
                                sx={{
                                    mr: 1
                                }}
                            />
                            <Typography style={{ color: 'white' }}>tests</Typography>
                        </Box>
                    }
                >
                    {Object.keys(tests).map((fileName) => (
                        <TreeItem
                            key={fileName}
                            itemId={fileName}
                            label={
                                <Box
                                    sx={{
                                        display: 'flex',
                                        alignItems: 'center'
                                    }}
                                >
                                    <InsertDriveFileIcon
                                        sx={{
                                            mr: 1
                                        }}
                                    />
                                    <Typography style={{ color: 'white' }}>{fileName}</Typography>
                                </Box>
                            }
                            onClick={() => {
                                editorRef.current.setValue(tests[fileName]);
                                editorRef.current.file = {
                                    fileName,
                                    type: 'test'
                                };
                                setCurrentFile({
                                    fileName,
                                    type: 'test',
                                    content: tests[fileName]
                                });
                            }}
                        />
                    ))}
                </TreeItem>
                <TreeItem
                    itemId="toml"
                    label={
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center'
                            }}
                        >
                            <InsertDriveFileIcon
                                sx={{
                                    mr: 1
                                }}
                            />
                            <Typography style={{ color: 'white' }}>Move.toml</Typography>
                        </Box>
                    }
                    onClick={() => {
                        editorRef.current.setValue(toml);
                        setCurrentFile({ fileName: 'Move.toml', type: 'toml', content: toml });
                    }}
                />
            </SimpleTreeView>
        </Box>
    );
}

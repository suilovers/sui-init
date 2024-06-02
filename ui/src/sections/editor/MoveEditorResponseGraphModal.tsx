import { Box, Modal } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { Graph } from 'jsoncrack-react';

interface MoveEditorResponseGraphModalProps {
    response: Object;
    onClose: () => void;
}

const useStyles = makeStyles({
    modal: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: 'calc(50vw) !important',
        height: 'calc(50vh) !importatnt',
        margin: 'auto'
    }
});

export default function MoveEditorResponseGraphModal({ response, onClose }: MoveEditorResponseGraphModalProps) {
    const isAvailable = JSON.stringify(response) !== '{}';
    const classes = useStyles();
    console.log(response);
    return (
        <Modal key="graph-modal" open={isAvailable} className={classes.modal} onClose={onClose}>
            <Box
                sx={{
                    width: 'calc(50vw)',
                    height: 'calc(50vh)',
                    backgroundColor: '#2a2a2a',
                    borderRadius: 1
                }}
            >
                <Graph
                    style={{
                        width: '100%',
                        height: '100%'
                    }}
                    id="graph"
                    json={JSON.stringify(response)}
                />
            </Box>
        </Modal>
    );
}

import WaterDropIcon from '@mui/icons-material/WaterDrop';
import { AppBar, Button, Toolbar } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { useNavigate } from 'react-router-dom';
import { PATH_MAIN } from '../routes/paths';
import CustomSwitchEnvDropdown from './CustomSwitchEnvDropdown';
const drawerWidth = 240;
const useStyles = makeStyles(() => ({
    moveEditorButton: {
        marginRight: '16px !important'
    }
}));
export default function CustomAppBar() {
    const classes = useStyles();
    const navigate = useNavigate();
    return (
        <AppBar
            position="fixed"
            sx={{
                width: `calc(100% - ${drawerWidth}px)`,
                ml: `${drawerWidth}px`,
                display: 'flex',
                alignItems: 'end'
            }}
        >
            <Toolbar>
                <Button
                    variant="contained"
                    className={classes.moveEditorButton}
                    onClick={() => navigate(PATH_MAIN.dashboard.moveEditor())}
                    endIcon={<WaterDropIcon />}
                >
                    Open Move Editor
                </Button>
                <CustomSwitchEnvDropdown />
            </Toolbar>
        </AppBar>
    );
}

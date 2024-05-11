import { AppBar, Theme, Toolbar } from '@mui/material';
import { makeStyles } from '@mui/styles';
import CustomSwitchEnvDropdown from './CustomSwitchEnvDropdown';

const drawerWidth = 240;
const useStyles = makeStyles((theme: Theme) => ({}));
export default function CustomAppBar() {
    const classes = useStyles();
    return (
        <AppBar
            position="fixed"
            sx={{
                width: `calc(100% - ${drawerWidth}px)`,
                ml: `${drawerWidth}px`,
                display: 'flex',
                alignItems: "end",
            }}
        >
            <Toolbar>
                <CustomSwitchEnvDropdown />
            </Toolbar>
        </AppBar>
    );
}

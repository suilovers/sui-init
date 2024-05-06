import RadioButtonCheckedRoundedIcon from '@mui/icons-material/RadioButtonCheckedRounded';
import { ListItemIcon } from '@mui/material';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import { useLoadCommands } from './hooks/useLoadCommands';

const drawerWidth = 240;

export default function CustomSider() {
    const { status, commands } = useLoadCommands();

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                        boxSizing: 'border-box'
                    }
                }}
                variant="permanent"
                anchor="left"
            >
                <Toolbar>
                    <h2>SUI Dashboard</h2>
                </Toolbar>
                <Divider />
                <List>
                    {commands.map((command) => (
                        <ListItem key={command.name} button>
                            <ListItemButton>
                                <ListItemIcon>
                                    <RadioButtonCheckedRoundedIcon />
                                </ListItemIcon>
                                <ListItemText primary={command.name} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Drawer>
        </Box>
    );
}

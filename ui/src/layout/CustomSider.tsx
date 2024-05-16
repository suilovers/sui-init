import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Toolbar from '@mui/material/Toolbar';
import CustomAppBar from './CustomAppBar';
import CustomSiderDropdownButton from './CustomSiderDropdownButton';
import { useLoadCommands } from './hooks/useLoadCommands';

const drawerWidth = 240;

export default function CustomSider() {
    const { commands } = useLoadCommands();
    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <CustomAppBar />
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                        boxSizing: 'border-box',
                        '-ms-overflow-style': 'none',
                        scrollbarWidth: 'none'
                    }
                }}
                variant="permanent"
                anchor="left"
            >
                <Toolbar>
                    <h2>SUI Dashboard</h2>
                </Toolbar>
                <Divider />

                <List
                    component="nav"
                    sx={{
                        width: '100%',
                        maxWidth: 360,
                        bgcolor: 'background.paper'
                    }}
                    aria-labelledby="nested-list-subheader"
                >
                    {commands.map((command) => (
                        <CustomSiderDropdownButton key={command.name} command={command} />
                    ))}
                </List>
            </Drawer>
        </Box>
    );
}

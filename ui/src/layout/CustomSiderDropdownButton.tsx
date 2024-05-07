import { ExpandLess, ExpandMore } from '@mui/icons-material';
import RadioButtonCheckedRoundedIcon from '@mui/icons-material/RadioButtonCheckedRounded';
import { Collapse, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useToggle } from '../hooks/useToggle';
import { CommandDTO } from '../types/sui/response';

interface CustomSiderDropdownButtonProps {
    command: CommandDTO;
}

export default function CustomSiderDropdownButton({ command }: CustomSiderDropdownButtonProps) {
    const [open, setOpen] = useToggle(true);
    const navigate = useNavigate();
    return (
        <>
            <ListItem key={command.name}>
                <ListItemButton onClick={setOpen}>
                    <ListItemIcon>
                        <RadioButtonCheckedRoundedIcon />
                    </ListItemIcon>
                    <ListItemText primary={command.name} />
                    {open ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
            </ListItem>
            {command.childs.length > 0 && (
                <Collapse in={open} timeout="auto" unmountOnExit>
                    <List component="div" disablePadding>
                        {command.childs.map((command) => (
                            <ListItemButton key={command.name} sx={{ pl: 4 }} onClick={() => navigate(command.path)}>
                                <ListItemText primary={command.name} />
                            </ListItemButton>
                        ))}
                    </List>
                </Collapse>
            )}
        </>
    );
}

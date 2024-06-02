import { Alert, Container, Snackbar } from '@mui/material';
import { Outlet } from 'react-router-dom';
import { useShowSnackbar } from '../hooks/useToggleSnackbar';
import CustomSider from './CustomSider';

export default function CustomLayoutView() {
    const { open, options } = useShowSnackbar();
    console.log('CustomLayoutView', open, options)
    return (
        <Container>
            <CustomSider />
            <Outlet />
            <Snackbar open={open} autoHideDuration={5000}>
                <Alert severity={options.severity} variant="filled">
                    {options.message}
                </Alert>
            </Snackbar>
        </Container>
    );
}

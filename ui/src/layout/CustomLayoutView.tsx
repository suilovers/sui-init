import { Container } from '@mui/material';
import { Outlet } from 'react-router-dom';
import CustomSider from './CustomSider';

export default function CustomLayoutView() {
    return (
        <Container>
            <CustomSider />
            <Outlet />
        </Container>
    );
}

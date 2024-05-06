import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Router } from './routes';

const darkTheme = createTheme({
    palette: {
        mode: 'dark'
    }
});

export default function App() {
    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <Router />  
        </ThemeProvider>
    );
}

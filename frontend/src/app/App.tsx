import { StrictMode } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { AppRouter } from './providers/AppRouter';
import { buildTheme } from 'shared/theme';
import { SessionProvider } from './providers/SessionProvider';
import { Header } from 'widgets/header';

export function App() {
  return (
    <StrictMode>
      <ThemeProvider theme={buildTheme()} defaultMode='system' noSsr>
        <CssBaseline />
        <SessionProvider>
          <Router>
            <Header />
            <AppRouter />
          </Router>
        </SessionProvider>
      </ThemeProvider>
    </StrictMode>
  );
}

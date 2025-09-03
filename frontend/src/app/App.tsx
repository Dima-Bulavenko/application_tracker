import { StrictMode } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { AppRouter } from './providers/AppRouter';
import { buildTheme } from 'shared/theme';
import { SessionProvider } from './providers/SessionProvider';
import { Header } from 'widgets/header';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export function App() {
  return (
    <StrictMode>
      <ThemeProvider theme={buildTheme()} defaultMode='system' noSsr>
        <CssBaseline />
        <QueryClientProvider client={queryClient}>
          <SessionProvider>
            <Router>
              <Header />
              <AppRouter />
            </Router>
          </SessionProvider>
        </QueryClientProvider>
      </ThemeProvider>
    </StrictMode>
  );
}

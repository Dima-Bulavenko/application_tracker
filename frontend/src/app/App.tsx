import { StrictMode, useMemo, useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { AppRouter } from './providers/AppRouter';
import { buildTheme } from 'shared/theme';
import { ColorModeContext } from './providers/ColorModeContext';
import { SessionProvider } from './providers/SessionProvider';

export function App() {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const theme = useMemo(() => buildTheme(mode), [mode]);
  const value = useMemo(
    () => ({
      mode,
      toggleMode: () => setMode((m) => (m === 'light' ? 'dark' : 'light')),
    }),
    [mode]
  );
  return (
    <StrictMode>
      <ColorModeContext.Provider value={value}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <SessionProvider>
            <Router>
              <AppRouter />
            </Router>
          </SessionProvider>
        </ThemeProvider>
      </ColorModeContext.Provider>
    </StrictMode>
  );
}

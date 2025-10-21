import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { buildTheme } from 'shared/theme';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuth } from 'shared/hooks/useAuth';
import { RouterProvider } from '@tanstack/react-router';
import { router } from './router';
import { AuthProvider } from './AuthProvider';
import { useLogin, useLogout } from 'features/user/hooks/useUser';

const queryClient = new QueryClient();

function InnerApp() {
  const auth = useAuth();
  const logout = useLogout();
  const login = useLogin();
  return (
    <RouterProvider
      router={router}
      context={{ auth: { ...auth, login, logout } }}
    />
  );
}

export function App() {
  return (
    <ThemeProvider theme={buildTheme()} defaultMode='system' noSsr>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <InnerApp />
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

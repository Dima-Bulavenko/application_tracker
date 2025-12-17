import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { buildTheme } from 'shared/theme';
import {
  MutationCache,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query';
import { useAuth } from 'shared/hooks/useAuth';
import { RouterProvider } from '@tanstack/react-router';
import { router } from './router';
import { AuthProvider } from './AuthProvider';
import {
  useLogin,
  useLoginWithGoogle,
  useLoginWithLinkedIn,
  useLogout,
} from 'features/user/hooks/useUser';
import { useEffect } from 'react';

const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onSuccess: (_data, _variables, _context, mutation) => {
      queryClient.invalidateQueries({
        queryKey: mutation.options.mutationKey,
      });
    },
  }),
});

function InnerApp() {
  const auth = useAuth();
  const logout = useLogout();
  const login = useLogin();
  const loginWithGoogle = useLoginWithGoogle();
  const loginWithLinkedIn = useLoginWithLinkedIn();
  useEffect(() => {
    router.invalidate();
  }, [auth.user]);

  return (
    <RouterProvider
      router={router}
      context={{
        auth: { ...auth, login, logout, loginWithGoogle, loginWithLinkedIn },
        queryClient,
      }}
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

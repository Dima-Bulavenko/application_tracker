import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import { activateUser } from 'shared/api/gen/sdk.gen';
import { AuthPage } from './AuthPage';
import { LinkButton } from 'shared/ui/LinkButton';
import { useQuery } from '@tanstack/react-query';
import { getRouteApi } from '@tanstack/react-router';

const routeApi = getRouteApi('/verify-email');

export function VerifyEmailPage() {
  const { token } = routeApi.useSearch();

  const { isLoading, isSuccess, isError, error } = useQuery({
    queryKey: ['activateUser', token],
    enabled: !!token,
    retry: false,
    queryFn: () => activateUser({ query: { token } }),
  });

  if (isLoading) {
    return (
      <AuthPage title='Verifying your email...'>
        <Stack spacing={3} alignItems='center'>
          <CircularProgress />
          <Typography variant='body2' color='text.secondary'>
            Please wait while we confirm your account.
          </Typography>
        </Stack>
      </AuthPage>
    );
  }

  if (isSuccess) {
    return (
      <AuthPage
        title='Email verified'
        subtitle='Your account has been activated. You can now sign in.'
        footerText="Don't have an account?"
        footerLinkText='Register'
        footerTo='/register'>
        <Stack spacing={3} alignItems='center'>
          <Typography variant='body2' color='text.secondary' textAlign='center'>
            Welcome aboard! Use your credentials to access your dashboard.
          </Typography>
          <LinkButton to='/sign-in' variant='contained' color='primary'>
            Go to Sign In
          </LinkButton>
        </Stack>
      </AuthPage>
    );
  }

  return (
    <AuthPage
      title='Verification failed'
      subtitle={
        (isError && error?.message) ||
        'We could not verify your email with this link.'
      }
      footerText='Need a new account?'
      footerLinkText='Register'
      footerTo='/register'>
      <Stack spacing={3} alignItems='center'>
        <Typography variant='body2' color='text.secondary' textAlign='center'>
          You can try signing in or registering again.
        </Typography>
        <LinkButton to='/sign-in' variant='contained'>
          Go to Sign In
        </LinkButton>
      </Stack>
    </AuthPage>
  );
}

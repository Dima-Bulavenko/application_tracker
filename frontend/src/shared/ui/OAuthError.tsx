import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';

import type { ReactNode } from 'react';

interface OAuthErrorProps {
  authButton: ReactNode;
}

export default function OAuthError({ authButton }: OAuthErrorProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: 3,
      }}>
      <Stack spacing={3} maxWidth={500} width='100%'>
        <Alert severity='error'>
          <AlertTitle>Authentication Error</AlertTitle>
          An error occurred during authentication. Please try signing in again.
        </Alert>

        <Typography variant='body2' color='text.secondary' textAlign='center'>
          If the problem persists, please contact support.
        </Typography>

        {authButton}
      </Stack>
    </Box>
  );
}

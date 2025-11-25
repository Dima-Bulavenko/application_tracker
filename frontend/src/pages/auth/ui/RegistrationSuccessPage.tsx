import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import EmailIcon from '@mui/icons-material/Email';

export function RegistrationSuccessPage() {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        padding: 3,
      }}>
      <Paper
        elevation={3}
        sx={{
          padding: 4,
          maxWidth: 500,
          width: '100%',
          textAlign: 'center',
        }}>
        <Stack spacing={3}>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              marginBottom: 2,
            }}>
            <EmailIcon
              sx={{
                fontSize: 64,
                color: 'primary.main',
              }}
            />
          </Box>

          <Typography variant='h4' component='h1' gutterBottom>
            Check Your Email
          </Typography>

          <Typography variant='body1' color='text.secondary'>
            We've sent an activation email to your inbox. Please check your
            email and click the activation link to complete your registration.
          </Typography>

          <Box
            sx={{
              backgroundColor: 'info.light',
              padding: 2,
              borderRadius: 1,
              marginTop: 2,
            }}>
            <Typography variant='body2' color='text.primary'>
              <strong>Didn't receive the email?</strong>
            </Typography>
            <Typography
              variant='body2'
              color='text.secondary'
              sx={{ marginTop: 1 }}>
              Try registering again with the same email address to resend the
              activation email.
            </Typography>
          </Box>
        </Stack>
      </Paper>
    </Box>
  );
}

import { useContext } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Paper from '@mui/material/Paper';
import { SessionContext } from 'shared/context/SessionContext';
import { LinkButton } from 'shared/ui/LinkButton';
export function HomePage() {
  const { token } = useContext(SessionContext);
  return (
    <Stack spacing={8} sx={{ py: 6 }}>
      {/* Hero Section */}
      <Box component='section' sx={{ textAlign: 'center' }}>
        <Typography variant='h2' component='h1' gutterBottom>
          Application Tracker
        </Typography>
        <Typography
          variant='h6'
          color='text.secondary'
          maxWidth={720}
          mx='auto'>
          Track and manage all your job applications in one organized workspace.
          Stay on top of every stage—from submission to interviews and offers.
        </Typography>
        <Stack direction='row' spacing={2} justifyContent='center' mt={4}>
          {token ? (
            <LinkButton to='/dashboard' variant='contained' color='primary'>
              Go to Dashboard
            </LinkButton>
          ) : (
            <>
              <LinkButton to='/register' variant='contained' color='primary'>
                Get Started
              </LinkButton>
              <LinkButton to='/sign-in' variant='outlined'>
                Sign In
              </LinkButton>
            </>
          )}
        </Stack>
      </Box>
      <Box component='section' maxWidth='lg' mx='auto' px={2}>
        <Box
          sx={{
            display: 'grid',
            gap: 4,
            gridTemplateColumns: {
              xs: '1fr',
              sm: 'repeat(2, 1fr)',
              md: 'repeat(3, 1fr)',
            },
          }}>
          {[
            {
              title: 'Centralized Tracking',
              body: 'Keep every application, company detail, and note in one place for quick reference and decision making.',
            },
            {
              title: 'Status Management',
              body: 'Monitor progress through each stage and never lose track of next steps or deadlines.',
            },
            {
              title: 'Actionable Insights',
              body: 'Coming soon: analytics to help you understand response rates and optimize your search.',
            },
          ].map((feature) => (
            <Paper
              key={feature.title}
              elevation={3}
              sx={{ p: 3, height: '100%' }}>
              <Typography variant='h6' gutterBottom>
                {feature.title}
              </Typography>
              <Typography variant='body2' color='text.secondary'>
                {feature.body}
              </Typography>
            </Paper>
          ))}
        </Box>
      </Box>

      {/* Auth Prompt */}
      {!token && (
        <Box component='section' textAlign='center'>
          <Typography variant='subtitle1' gutterBottom>
            Create a free account to start organizing your applications.
          </Typography>
          <LinkButton to='/register' variant='contained'>
            Create Account
          </LinkButton>
        </Box>
      )}
    </Stack>
  );
}

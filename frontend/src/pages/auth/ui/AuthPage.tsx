import { Box, Paper, Stack, Typography, Divider, Link } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import type { SxProps, Theme } from '@mui/material/styles';

export interface AuthPageProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footerText?: string;
  footerLinkText?: string;
  footerTo?: string;
  sx?: SxProps<Theme>;
}

export function AuthPage({
  title,
  subtitle,
  children,
  footerText,
  footerLinkText,
  footerTo,
  sx,
}: AuthPageProps) {
  return (
    <Box
      component='section'
      sx={(theme) => ({
        minHeight: '100dvh',
        display: 'grid',
        placeItems: 'center',
        px: 2,
        py: 8,
        backgroundColor: 'background.default',
        ...((typeof sx === 'function' ? sx(theme) : sx) as object),
      })}>
      <Paper elevation={4} sx={{ p: 4, width: '100%', maxWidth: 480 }}>
        <Stack spacing={3}>
          <Stack spacing={0.5}>
            <Typography variant='h4' component='h1'>
              {title}
            </Typography>
            {subtitle && (
              <Typography variant='body2' color='text.secondary'>
                {subtitle}
              </Typography>
            )}
          </Stack>

          {children}

          {(footerText || (footerLinkText && footerTo)) && (
            <>
              <Divider />
              <Typography
                variant='body2'
                color='text.secondary'
                textAlign='center'>
                {footerText}{' '}
                {footerLinkText && footerTo && (
                  <Link component={RouterLink} to={footerTo} underline='hover'>
                    {footerLinkText}
                  </Link>
                )}
              </Typography>
            </>
          )}
        </Stack>
      </Paper>
    </Box>
  );
}

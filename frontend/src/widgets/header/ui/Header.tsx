import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { Link as RouterLink } from '@tanstack/react-router';
import { ColorModeToggler } from 'shared/ui/ColorModeToggler';
import { AccountMenu } from 'features/user/ui/AccountMenu';
import { getRouteApi } from '@tanstack/react-router';

const routeApi = getRouteApi('__root__');

export function Header() {
  const {
    auth: { user },
  } = routeApi.useRouteContext();
  return (
    <AppBar position='sticky' color='default' elevation={0}>
      <Toolbar sx={{ gap: 1, minHeight: 64 }}>
        <Box
          component={RouterLink}
          to='/'
          sx={{
            display: 'flex',
            alignItems: 'center',
            textDecoration: 'none',
            '&:hover': {
              opacity: 0.8,
            },
            transition: 'opacity 0.2s',
          }}>
          <Box
            component='img'
            src='/logo.svg'
            alt='Application Tracker'
            sx={{
              height: 30,
              width: 70,
            }}
          />
        </Box>

        <Box sx={{ flex: 1 }} />

        <Stack direction='row' spacing={1} alignItems='center'>
          {user ? (
            <AccountMenu />
          ) : (
            <>
              <Button
                size='small'
                color='primary'
                variant='text'
                component={RouterLink}
                to='/sign-in'>
                Login
              </Button>
              <Button
                size='small'
                color='primary'
                variant='contained'
                component={RouterLink}
                to='/register'>
                Register
              </Button>
            </>
          )}
        </Stack>

        <ColorModeToggler />
      </Toolbar>
    </AppBar>
  );
}

export default Header;

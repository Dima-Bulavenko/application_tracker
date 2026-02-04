import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import { ColorModeToggler } from 'shared/ui/ColorModeToggler';
import { AccountMenu } from 'features/user/ui/AccountMenu';
import { getRouteApi } from '@tanstack/react-router';
import { LinkButton } from 'shared/ui/LinkButton';

const routeApi = getRouteApi('__root__');

export function Header() {
  const {
    auth: { user },
  } = routeApi.useRouteContext();
  return (
    <AppBar position='sticky' color='default' elevation={0}>
      <Toolbar sx={{ gap: 1, minHeight: 64 }}>
        <LinkButton
          to={user ? '/dashboard' : '/'}
          sx={{ backdropFilter: 'none' }}>
          <Box
            component='img'
            src='/logo.svg'
            alt='Application Tracker'
            sx={{
              height: 30,
              width: 70,
            }}
          />
        </LinkButton>
        <Box sx={{ flex: 1 }} />

        <Stack direction='row' spacing={1} alignItems='center'>
          {user ? (
            <AccountMenu />
          ) : (
            <>
              <LinkButton
                size='small'
                color='primary'
                variant='text'
                to='/sign-in'>
                Login
              </LinkButton>
              <LinkButton
                size='small'
                color='primary'
                variant='contained'
                to='/register'>
                Register
              </LinkButton>
            </>
          )}
        </Stack>

        <ColorModeToggler />
      </Toolbar>
    </AppBar>
  );
}

export default Header;

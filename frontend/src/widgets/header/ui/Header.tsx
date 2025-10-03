import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { Link as RouterLink } from 'react-router-dom';
import { useSession } from 'shared/hooks';
import { ColorModeToggler } from 'shared/ui';
import { AccountMenu } from 'features/user/ui';

export function Header() {
  const { token, isFetching } = useSession();
  return (
    <AppBar position='sticky' color='default' elevation={0}>
      <Toolbar sx={{ gap: 1, minHeight: 64 }}>
        <Typography
          variant='h6'
          component={RouterLink}
          to='/'
          sx={{ textDecoration: 'none', color: 'inherit' }}>
          App Tracker
        </Typography>

        <Box sx={{ flex: 1 }} />

        <Stack direction='row' spacing={1} alignItems='center'>
          {token || isFetching ? (
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

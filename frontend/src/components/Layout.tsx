import { Outlet, NavLink } from 'react-router-dom';
import { Box } from '@mui/material';

export function Layout() {
  return (
    <>
      <Box component='header'>
        <Box component='div'>
          <NavLink to='/'>Home</NavLink>
          <NavLink to='/register'>Sign Up</NavLink>
          <NavLink to='/login'>Sign In</NavLink>
        </Box>
      </Box>
      <Box component='main'>
        <Outlet />
      </Box>
    </>
  );
}

import Logout from '@mui/icons-material/Logout';
import Avatar from '@mui/material/Avatar';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Tooltip from '@mui/material/Tooltip';
import { useState } from 'react';
import { getRouteApi } from '@tanstack/react-router';
import { LinkButton } from 'shared/ui/LinkButton';

const MenuStyle = {
  paper: {
    elevation: 0,
    sx: {
      overflow: 'visible',
      filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
      mt: 1.5,
      '& .MuiAvatar-root': {
        width: 32,
        height: 32,
        ml: -0.5,
        mr: 1,
      },
      '&::before': {
        content: '""',
        display: 'block',
        position: 'absolute',
        top: 0,
        right: 14,
        width: 10,
        height: 10,
        bgcolor: 'background.paper',
        transform: 'translateY(-50%) rotate(45deg)',
        zIndex: 0,
      },
    },
  },
};

const routeApi = getRouteApi('__root__');

export function AccountMenu() {
  const {
    auth: { user, logout },
  } = routeApi.useRouteContext();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const navigate = routeApi.useNavigate();
  const open = !!anchorEl;
  const handleClick = (e: React.MouseEvent<HTMLElement>) =>
    setAnchorEl(e.currentTarget);
  const handleClose = () => setAnchorEl(null);

  if (!user) return null;
  return (
    <>
      <Tooltip title='Account settings'>
        <IconButton
          onClick={handleClick}
          size='small'
          sx={{ ml: 2 }}
          aria-controls={open ? 'account-menu' : undefined}
          aria-haspopup='true'
          aria-expanded={open ? 'true' : undefined}>
          <Avatar sx={{ width: 32, height: 32 }}>
            {user.username.charAt(0).toUpperCase()}
          </Avatar>
        </IconButton>
      </Tooltip>
      <Menu
        anchorEl={anchorEl}
        id='account-menu'
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        slotProps={MenuStyle}
        transformOrigin={{ horizontal: 'center', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'center', vertical: 'bottom' }}>
        <Divider />
        <MenuItem onClick={handleClose}>
          <LinkButton
            to='/profile'
            sx={{
              display: 'flex',
              alignItems: 'center',
              color: 'inherit',
              padding: 0,
            }}>
            <Avatar /> Profile
          </LinkButton>
        </MenuItem>
        <Divider />
        <MenuItem
          onClick={() => {
            logout().finally(() => {
              handleClose();
              navigate({ to: '/' });
            });
          }}>
          <ListItemIcon>
            <Logout fontSize='small' />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>
    </>
  );
}

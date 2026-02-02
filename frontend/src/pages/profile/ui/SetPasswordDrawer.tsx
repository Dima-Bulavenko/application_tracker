import { Suspense } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import Divider from '@mui/material/Divider';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';
import { SetPasswordForm } from './SetPasswordForm';
import { getCurrentUser } from 'shared/api/gen';
import { getRouteApi } from '@tanstack/react-router';

interface SetPasswordProps {
  open: boolean;
  onClose: () => void;
}

const routeApi = getRouteApi('/_authenticated');

export function SetPasswordDrawer({ open, onClose }: SetPasswordProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const {
    auth: { setUser },
  } = routeApi.useRouteContext();
  const onSuccess = async () => {
    const { data } = await getCurrentUser();
    setUser(data);
    onClose();
  };

  return (
    <Drawer
      anchor='right'
      open={open}
      onClose={onClose}
      slotProps={{
        root: {
          keepMounted: true,
        },
        paper: {
          sx: {
            width: isMobile ? '85vw' : '500px',
            maxWidth: '500px',
          },
        },
      }}>
      <Box sx={{ p: 3, height: '100%' }}>
        <Typography variant='h5' component='h2' gutterBottom>
          Set Password
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Suspense fallback={<SuspenseFallback />}>
          {open && <SetPasswordForm onSuccess={onSuccess} />}
        </Suspense>
      </Box>
    </Drawer>
  );
}

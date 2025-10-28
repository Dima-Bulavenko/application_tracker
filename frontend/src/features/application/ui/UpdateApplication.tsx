import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Drawer from '@mui/material/Drawer';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import EditIcon from '@mui/icons-material/Edit';
import { Suspense, useState } from 'react';
import { lazyImport } from 'shared/lib/lazyLoad';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';
import type { ApplicationRead } from 'shared/api/gen/types.gen';

type UpdateApplicationProps = {
  application: ApplicationRead;
};

const { UpdateApplicationForm } = lazyImport(
  () => import('./UpdateApplicationForm'),
  'UpdateApplicationForm'
);

export function UpdateApplication({ application }: UpdateApplicationProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleClose = () => setDrawerOpen(false);

  return (
    <>
      <Button
        startIcon={<EditIcon />}
        variant='contained'
        color='primary'
        onClick={() => setDrawerOpen(true)}>
        Edit
      </Button>
      <Drawer
        anchor='right'
        open={drawerOpen}
        onClose={handleClose}
        ModalProps={{ keepMounted: true }}
        slotProps={{
          paper: {
            sx: {
              width: isMobile ? '85vw' : '600px',
              maxWidth: '600px',
            },
          },
        }}>
        <Box sx={{ p: 3, height: '100%' }}>
          <Typography variant='h5' component='h2' gutterBottom>
            Update Application
          </Typography>
          <Divider sx={{ mb: 3 }} />
          <Suspense fallback={<SuspenseFallback />}>
            {drawerOpen && <UpdateApplicationForm {...application} />}
          </Suspense>
        </Box>
      </Drawer>
    </>
  );
}

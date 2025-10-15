import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import AddIcon from '@mui/icons-material/Add';
import { Suspense, useState } from 'react';
import { lazyImport } from 'shared/lib/lazyLoad';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';

const { CreateApplicationForm } = lazyImport(
  () => import('./CreateApplicationForm'),
  'CreateApplicationForm'
);

export function CreateApplication() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleClose = () => setDrawerOpen(false);

  return (
    <>
      <Box
        sx={{
          position: 'fixed',
          bottom: theme.spacing(12),
          right: theme.spacing(2),
          zIndex: theme.zIndex.appBar,
        }}>
        <IconButton
          sx={{ backgroundColor: 'primary.main' }}
          size='medium'
          onClick={() => setDrawerOpen(true)}>
          <AddIcon fontSize='inherit' />
        </IconButton>
      </Box>
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
            Create Application
          </Typography>
          <Divider sx={{ mb: 3 }} />
          <Suspense fallback={<SuspenseFallback />}>
            {drawerOpen && <CreateApplicationForm />}
          </Suspense>
        </Box>
      </Drawer>
    </>
  );
}

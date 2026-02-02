import { useState } from 'react';
import Paper from '@mui/material/Paper';
import { SectionHeader } from './SectionHeader';
import { SetPasswordDrawer } from './SetPasswordDrawer';

export function SetPasswordSection() {
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleOpenDrawer = () => setDrawerOpen(true);
  const handleCloseDrawer = () => setDrawerOpen(false);

  return (
    <>
      <Paper elevation={1} sx={{ p: 3 }}>
        <SectionHeader
          title='Set Password'
          subtitle='Create a password for your account'
          onEditClick={handleOpenDrawer}
        />
        <SetPasswordDrawer open={drawerOpen} onClose={handleCloseDrawer} />
      </Paper>
    </>
  );
}

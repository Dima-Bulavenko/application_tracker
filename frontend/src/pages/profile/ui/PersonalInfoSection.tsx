import { useState } from 'react';
import Paper from '@mui/material/Paper';
import { getRouteApi } from '@tanstack/react-router';
import { SectionHeader } from './SectionHeader';
import { UserInfoList } from './UserInfoList';
import { EditDrawer } from './EditDrawer';

const routeApi = getRouteApi('/_authenticated');

export function PersonalInfoSection() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const {
    auth: { user },
  } = routeApi.useRouteContext();

  const handleOpenDrawer = () => setDrawerOpen(true);
  const handleCloseDrawer = () => setDrawerOpen(false);

  return (
    <>
      <Paper elevation={1} sx={{ p: 3 }}>
        <SectionHeader
          title='Personal Information'
          subtitle='Your profile details'
          onEditClick={handleOpenDrawer}
        />
        <UserInfoList user={user} />
      </Paper>

      <EditDrawer open={drawerOpen} onClose={handleCloseDrawer} />
    </>
  );
}

import { Container, Stack } from '@mui/material';
import ApplicationList from 'entities/application/ui/ApplicationList';
import { useState } from 'react';
import {
  CreateApplicationButton,
  CreateApplicationDialog,
} from 'features/create-application';

export function DashboardPage() {
  const [open, setOpen] = useState(false);
  return (
    <Container sx={{ py: 2 }}>
      <Stack direction='row' justifyContent='flex-end' mb={2}>
        <CreateApplicationButton onClick={() => setOpen(true)} />
      </Stack>
      <ApplicationList pageSize={10} />
      <CreateApplicationDialog open={open} onClose={() => setOpen(false)} />
    </Container>
  );
}

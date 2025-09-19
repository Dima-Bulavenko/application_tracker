import { Container, Stack } from '@mui/material';
import { useState } from 'react';
import {
  ApplicationListWidget,
  CreateApplicationButton,
  CreateApplicationDialog,
} from 'features/application';

export function DashboardPage() {
  const [open, setOpen] = useState(false);
  return (
    <Container sx={{ py: 2 }}>
      <Stack direction='row' justifyContent='flex-end' mb={2}>
        <CreateApplicationButton onClick={() => setOpen(true)} />
      </Stack>
      <ApplicationListWidget />
      <CreateApplicationDialog open={open} onClose={() => setOpen(false)} />
    </Container>
  );
}

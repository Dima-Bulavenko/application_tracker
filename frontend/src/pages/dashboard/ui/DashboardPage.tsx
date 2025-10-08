import { Container } from '@mui/material';
import { ApplicationListWidget, CreateApplication } from 'features/application';

export function DashboardPage() {
  return (
    <Container sx={{ py: 2 }}>
      <ApplicationListWidget />
      <CreateApplication />
    </Container>
  );
}

import Container from '@mui/material/Container';
import { ApplicationListWidget } from 'features/application/ui/ApplicationListWidget';
import { CreateApplication } from 'features/application/ui/CreateApplication';

export function DashboardPage() {
  return (
    <Container sx={{ py: 2 }}>
      <ApplicationListWidget />
      <CreateApplication />
    </Container>
  );
}

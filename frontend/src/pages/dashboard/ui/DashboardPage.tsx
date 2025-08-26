import { Container } from '@mui/material';
import ApplicationList from 'entities/application/ui/ApplicationList';

export function DashboardPage() {
  return (
    <Container sx={{ py: 2 }}>
      <ApplicationList pageSize={10} />
    </Container>
  );
}

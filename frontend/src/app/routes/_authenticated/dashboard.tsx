import { createFileRoute } from '@tanstack/react-router';
import { DashboardPage } from 'pages/dashboard/ui/DashboardPage';

export const Route = createFileRoute('/_authenticated/dashboard')({
  component: RouteComponent,
});

function RouteComponent() {
  return <DashboardPage />;
}

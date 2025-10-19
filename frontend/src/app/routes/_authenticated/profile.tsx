import { createFileRoute } from '@tanstack/react-router';
import { ProfilePage } from 'pages/profile/ui/ProfilePage';

export const Route = createFileRoute('/_authenticated/profile')({
  component: RouteComponent,
});

function RouteComponent() {
  return <ProfilePage />;
}

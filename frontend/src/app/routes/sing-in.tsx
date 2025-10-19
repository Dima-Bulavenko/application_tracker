import { createFileRoute } from '@tanstack/react-router';
import { SignInPage } from 'pages/auth/ui/SignInPage';

export const Route = createFileRoute('/sing-in')({
  component: RouteComponent,
});

function RouteComponent() {
  return <SignInPage />;
}

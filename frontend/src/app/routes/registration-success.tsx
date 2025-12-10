import { createFileRoute } from '@tanstack/react-router';
import { RegistrationSuccessPage } from 'pages/auth/ui/RegistrationSuccessPage';
import z from 'zod';

const userEmailSchema = z.object({
  registrationEmail: z.email(),
});

export const Route = createFileRoute('/registration-success')({
  validateSearch: userEmailSchema,
  component: RouteComponent,
});

function RouteComponent() {
  return <RegistrationSuccessPage />;
}

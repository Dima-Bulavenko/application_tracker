import { createFileRoute } from '@tanstack/react-router';
import { VerifyEmailPage } from 'pages/auth/ui/VerifyEmailPage';
import { z } from 'zod';

const verifyEmailSearchSchema = z.object({
  token: z.string().catch(''),
});

export const Route = createFileRoute('/verify-email')({
  validateSearch: verifyEmailSearchSchema,
  component: RouteComponent,
});

function RouteComponent() {
  return <VerifyEmailPage />;
}

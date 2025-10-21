import { createFileRoute } from '@tanstack/react-router';
import { SignInPage } from 'pages/auth/ui/SignInPage';
import { z } from 'zod';

const SignInSearchSchema = z.object({
  redirect: z.string().catch('/dashboard'),
});

export const Route = createFileRoute('/sign-in')({
  validateSearch: SignInSearchSchema,
  component: RouteComponent,
});

function RouteComponent() {
  return <SignInPage />;
}

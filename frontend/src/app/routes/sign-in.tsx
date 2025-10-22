import { createFileRoute, redirect } from '@tanstack/react-router';
import { SignInPage } from 'pages/auth/ui/SignInPage';
import { z } from 'zod';

const SignInSearchSchema = z.object({
  redirect: z.string().catch('/dashboard'),
});

export const Route = createFileRoute('/sign-in')({
  validateSearch: SignInSearchSchema,
  beforeLoad: ({ context, search }) => {
    if (context.auth.isAuthenticated) {
      throw redirect({ to: search.redirect, replace: true });
    }
  },
  component: RouteComponent,
});

function RouteComponent() {
  return <SignInPage />;
}

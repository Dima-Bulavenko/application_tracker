import { createFileRoute, redirect } from '@tanstack/react-router';
import { SignInPage } from 'pages/auth/ui/SignInPage';
import { z } from 'zod';
import type { SearchSchemaInput } from '@tanstack/react-router';

const SignInSearchSchema = z.object({
  redirect: z.string().catch('/dashboard'),
});

type SignInSearch = z.infer<typeof SignInSearchSchema>;

export const Route = createFileRoute('/sign-in')({
  validateSearch: (search: Partial<SignInSearch> & SearchSchemaInput) =>
    SignInSearchSchema.parse(search),
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

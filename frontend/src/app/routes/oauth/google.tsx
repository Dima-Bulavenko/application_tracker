import { createFileRoute, Navigate } from '@tanstack/react-router';
import { zGoogleCallbackData } from 'shared/api/gen/zod.gen';
import OAuthError from 'shared/ui/OAuthError';
import GoogleAuthorizationButton from 'shared/ui/GoogleAuthorizationButton';

const zSearchPramsSchema = zGoogleCallbackData.shape.query;

export const Route = createFileRoute('/oauth/google')({
  validateSearch: zSearchPramsSchema,
  loaderDeps: ({ search }) => search,
  loader: async ({ deps, context }) => {
    const { code, state } = deps;
    const { loginWithGoogle } = context.auth;
    const res = await loginWithGoogle(code, state);
    return res;
  },
  component: RouteComponent,
  errorComponent: ErrorRouteComponent,
});

function RouteComponent() {
  return <Navigate to={'/dashboard'} replace={true} />;
}

function ErrorRouteComponent() {
  return (
    <OAuthError authButton={<GoogleAuthorizationButton action='sign-in' />} />
  );
}

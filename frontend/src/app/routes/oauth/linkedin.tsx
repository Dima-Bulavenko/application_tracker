import { createFileRoute, Navigate } from '@tanstack/react-router';
import { zLinkedinCallbackData } from 'shared/api/gen/zod.gen';
import OAuthError from 'shared/ui/OAuthError';
import LinkedInAuthorizationButton from 'shared/ui/LinkedInAuthorizationButton';

const zSearchPramsSchema = zLinkedinCallbackData.shape.query;

export const Route = createFileRoute('/oauth/linkedin')({
  validateSearch: zSearchPramsSchema,
  loaderDeps: ({ search }) => search,
  loader: async ({ deps, context }) => {
    const { code, state } = deps;
    const { loginWithLinkedIn } = context.auth;
    const res = await loginWithLinkedIn(code, state);
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
    <OAuthError authButton={<LinkedInAuthorizationButton action='sign-in' />} />
  );
}

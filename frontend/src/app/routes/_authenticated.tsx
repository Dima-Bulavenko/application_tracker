import { createFileRoute, redirect, Outlet } from '@tanstack/react-router';

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: ({ context, location }) => {
    const {
      auth: { user, isAuthenticated, setUser },
    } = context;
    if (!user) {
      throw redirect({ to: '/sign-in', search: { redirect: location.href } });
    }
    return {
      auth: { user, isAuthenticated, setUser },
    };
  },
  component: RouteComponent,
});

function RouteComponent() {
  return <Outlet />;
}

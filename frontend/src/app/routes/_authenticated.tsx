import { createFileRoute, redirect, Outlet } from '@tanstack/react-router';

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: ({ context, location }) => {
    const {
      auth: { user, isAuthenticated, logout },
    } = context;
    if (!user || !isAuthenticated) {
      throw redirect({ to: '/sing-in', search: { redirect: location.href } });
    }
    return {
      auth: { user, isAuthenticated, logout },
    };
  },
  component: RouteComponent,
});

function RouteComponent() {
  return <Outlet />;
}

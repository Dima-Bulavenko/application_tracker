import { Suspense } from 'react';
import { createRootRouteWithContext, Outlet } from '@tanstack/react-router';
import { Header } from 'widgets/header/ui/Header';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools';
import type { AuthContextType } from 'shared/context/AuthContext';
import type { AccessTokenResponse, UserLogin } from 'shared/api/gen';

interface RouterContext {
  auth: AuthContextType & {
    logout: () => Promise<void>;
    login: (data: UserLogin) => Promise<AccessTokenResponse>;
  };
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: IndexComponent,
});

function IndexComponent() {
  return (
    <>
      <Header />
      <Suspense fallback={<SuspenseFallback />}>
        <Outlet />
      </Suspense>
      <TanStackRouterDevtools position='bottom-right' initialIsOpen={false} />
    </>
  );
}

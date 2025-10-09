import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from 'widgets/header';
import { SuspenseFallback } from 'shared/ui';

export function Layout() {
  return (
    <>
      <Header />
      <Suspense fallback={<SuspenseFallback />}>
        <Outlet />
      </Suspense>
    </>
  );
}

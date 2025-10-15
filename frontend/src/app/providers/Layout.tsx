import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from 'widgets/header/ui/Header';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';

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

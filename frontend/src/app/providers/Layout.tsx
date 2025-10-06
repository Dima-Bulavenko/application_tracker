import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from 'widgets/header';

export function Layout() {
  return (
    <>
      <Header />
      <Suspense fallback={<div>Loading...</div>}>
        <Outlet />
      </Suspense>
    </>
  );
}

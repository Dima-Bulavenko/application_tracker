import { Route, Routes } from 'react-router-dom';
import { PublicOnly } from './route-guards/PublicOnly';
import { RequireAuth } from './route-guards/RequireAuth';
import { lazyImport } from 'shared/lib';
import { Layout } from './Layout';

const { HomePage } = lazyImport(() => import('pages/home'), 'HomePage');
const { DashboardPage } = lazyImport(
  () => import('pages/dashboard'),
  'DashboardPage'
);
const { SignInPage } = lazyImport(() => import('pages/auth'), 'SignInPage');
const { RegisterPage } = lazyImport(() => import('pages/auth'), 'RegisterPage');
const { VerifyEmailPage } = lazyImport(
  () => import('pages/auth'),
  'VerifyEmailPage'
);
const { PageNotFound } = lazyImport(() => import('shared/ui'), 'PageNotFound');

export function AppRouter() {
  return (
    <Routes>
      <Route path='/' element={<Layout />}>
        <Route path='/' element={<HomePage />} />
        <Route
          path='/dashboard'
          element={
            <RequireAuth>
              <DashboardPage />
            </RequireAuth>
          }
        />
        <Route
          path='/sign-in'
          element={
            <PublicOnly>
              <SignInPage />
            </PublicOnly>
          }
        />
        <Route
          path='/register'
          element={
            <PublicOnly>
              <RegisterPage />
            </PublicOnly>
          }
        />
        <Route
          path='/verify-email'
          element={
            <PublicOnly>
              <VerifyEmailPage />
            </PublicOnly>
          }
        />
        <Route path='*' element={<PageNotFound />} />
      </Route>
    </Routes>
  );
}

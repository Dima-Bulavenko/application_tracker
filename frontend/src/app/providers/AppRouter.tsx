import { Route, Routes } from 'react-router-dom';
import { PublicOnly } from './route-guards/PublicOnly';
import { RequireAuth } from './route-guards/RequireAuth';
import { lazyImport } from 'shared/lib/lazyLoad';
import { Layout } from './Layout';

const { HomePage } = lazyImport(
  () => import('pages/home/ui/HomePage'),
  'HomePage'
);
const { DashboardPage } = lazyImport(
  () => import('pages/dashboard/ui/DashboardPage'),
  'DashboardPage'
);
const { SignInPage } = lazyImport(
  () => import('pages/auth/ui/SignInPage'),
  'SignInPage'
);
const { RegisterPage } = lazyImport(
  () => import('pages/auth/ui/RegisterPage'),
  'RegisterPage'
);
const { VerifyEmailPage } = lazyImport(
  () => import('pages/auth/ui/VerifyEmailPage'),
  'VerifyEmailPage'
);
const { PageNotFound } = lazyImport(
  () => import('shared/ui/PageNotFound'),
  'PageNotFound'
);

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

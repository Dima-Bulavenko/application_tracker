import { Route, Routes } from 'react-router-dom';
import { HomePage } from 'pages/home';
import { SignInPage, RegisterPage } from 'pages/auth';
import { DashboardPage } from 'pages/dashboard';
import { PageNotFound } from 'shared/ui';
import { PublicOnly } from './route-guards/PublicOnly';
import { RequireAuth } from './route-guards/RequireAuth';

export function AppRouter() {
  return (
    <Routes>
      <Route path='/'>
        <Route index element={<HomePage />} />
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
        <Route path='*' element={<PageNotFound />} />
      </Route>
    </Routes>
  );
}

import { Navigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { SessionContext } from 'shared/context/SessionContext';

export function RequireAuth({ children }: { children: JSX.Element }) {
  const { isAuthenticated } = useContext(SessionContext);
  const location = useLocation();
  return isAuthenticated ? (
    children
  ) : (
    <Navigate to='/sign-in' replace state={{ from: location }} />
  );
}

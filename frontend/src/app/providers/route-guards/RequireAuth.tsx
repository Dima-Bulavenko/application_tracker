import { Navigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { SessionContext } from 'shared/context/SessionContext';

export function RequireAuth({ children }: { children: JSX.Element }) {
  const { token } = useContext(SessionContext);
  const location = useLocation();
  return token ? (
    children
  ) : (
    <Navigate to='/sign-in' replace state={{ from: location }} />
  );
}

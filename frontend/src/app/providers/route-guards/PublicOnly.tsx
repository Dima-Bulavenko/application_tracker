import { Navigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { SessionContext } from 'shared/context/SessionContext';

export function PublicOnly({ children }: { children: JSX.Element }) {
  const { token } = useContext(SessionContext);
  const location = useLocation();
  return token ? (
    <Navigate to='/dashboard' replace state={{ from: location }} />
  ) : (
    children
  );
}

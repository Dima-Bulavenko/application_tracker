import { Navigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { SessionContext } from 'shared/context/SessionContext';

export function PublicOnly({ children }: { children: JSX.Element }) {
  const { isAuthenticated } = useContext(SessionContext);
  const location = useLocation();
  return isAuthenticated ? (
    <Navigate to='/' replace state={{ from: location }} />
  ) : (
    children
  );
}

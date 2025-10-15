import { Navigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { SessionContext } from 'shared/context/SessionContext';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';

export function RequireAuth({ children }: { children: JSX.Element }) {
  const { token, isFetching } = useContext(SessionContext);
  console.log('in RequireAuth');
  const location = useLocation();
  if (isFetching) return <SuspenseFallback />;
  if (!token)
    return <Navigate to='/sign-in' replace state={{ from: location }} />;
  return children;
}

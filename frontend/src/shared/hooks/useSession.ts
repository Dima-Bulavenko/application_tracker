import { useContext } from 'react';
import { SessionContext } from 'shared/context';

export function useSession() {
  const { user, token, isFetching, setUser, setToken } =
    useContext(SessionContext);
  if (setUser !== undefined && setToken !== undefined) {
    return { user, token, isFetching, setUser, setToken };
  }
  throw new Error('setToken and setUser must be set inside SessionProvider');
}

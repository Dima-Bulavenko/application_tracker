import { useContext } from 'react';
import { SessionContext } from 'shared/context';

export function useSession() {
  const { user, token, setUser, setToken } = useContext(SessionContext);
  if (setUser !== undefined && setToken !== undefined) {
    return { user, token, setUser, setToken };
  }
  throw new Error('setToken and setUser must be set inside SessionProvider');
}

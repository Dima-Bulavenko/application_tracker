import { useContext } from 'react';
import { SessionContext } from 'shared/context';

export function useSession() {
  const session = useContext(SessionContext);
  return session;
}

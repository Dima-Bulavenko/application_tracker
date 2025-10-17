import { useContext } from 'react';
import type { SessionContextType } from 'shared/context/SessionContext';
import { SessionContext } from 'shared/context/SessionContext';

type ActiveSession = Required<SessionContextType>;
type Session = Omit<SessionContextType, 'setToken' | 'setUser'> &
  Required<Pick<SessionContextType, 'setToken' | 'setUser'>>;

export function useSession() {
  const ctx = useContext(SessionContext);
  if (!ctx || !ctx.setToken || !ctx.setUser) {
    throw new Error('No session context found');
  }
  return ctx as Session;
}

export function useActiveSession() {
  const ctx = useContext(SessionContext);
  if (!ctx || !ctx.user || !ctx.token) {
    throw new Error('No active session found');
  }
  return ctx as ActiveSession;
}

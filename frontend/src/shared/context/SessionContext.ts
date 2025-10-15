import { createContext } from 'react';
import { UserRead } from 'shared/api/gen/types.gen';

export interface SessionContextType {
  readonly token?: string;
  readonly user?: UserRead;
  readonly isFetching?: boolean;
  setToken?: (token: string | undefined) => void;
  setUser?: (user: UserRead | undefined) => void;
}

export const SessionContext = createContext<SessionContextType>({});

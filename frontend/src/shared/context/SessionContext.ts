import React, { createContext } from 'react';
import { UserRead } from 'shared/api';

export interface SessionContextType {
  readonly token?: string;
  readonly user?: UserRead;
  setToken?: React.Dispatch<React.SetStateAction<string | undefined>>;
  setUser?: React.Dispatch<React.SetStateAction<UserRead | undefined>>;
}

export const SessionContext = createContext<SessionContextType>({});

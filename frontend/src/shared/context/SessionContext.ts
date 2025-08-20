import { createContext } from 'react';
import { UserRead, UserLogin } from 'shared/api';
import {
  login as sdkLogin,
  logout as sdkLogout,
  refreshToken as sdkRefresh,
} from 'shared/api/gen/sdk.gen';

type LoginReturn = ReturnType<typeof sdkLogin>;
type LogoutReturn = ReturnType<typeof sdkLogout>;
type RefreshReturn = ReturnType<typeof sdkRefresh>;

export interface SessionContextType {
  isAuthenticated: boolean;
  readonly token?: string; // read-only for consumers
  readonly user?: UserRead;
  login: (data: UserLogin) => LoginReturn;
  logout: () => LogoutReturn;
  refresh: () => RefreshReturn;
}

export const SessionContext = createContext<SessionContextType>({
  isAuthenticated: false,
  async login() {
    throw new Error('SessionContext not initialized');
  },
  async logout() {
    throw new Error('SessionContext not initialized');
  },
  async refresh() {
    throw new Error('SessionContext not initialized');
  },
});

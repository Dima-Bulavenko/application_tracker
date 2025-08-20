import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  login as apiLogin,
  logout as apiLogout,
  refreshToken,
  getCurrentUser,
  type UserRead,
  UserLogin,
} from 'shared/api';

import { SessionContext } from 'shared/context/SessionContext';

export function SessionProvider({ children }: React.PropsWithChildren<object>) {
  const [token, setToken] = useState<string | undefined>();
  const [user, setUser] = useState<UserRead | undefined>();

  const isAuthenticated = !!token;

  const fetchMe = useCallback(async (t: string) => {
    const res = await getCurrentUser({
      headers: { Authorization: `Bearer ${t}` },
    });
    if (res.status === 200 && res.data) {
      setUser(res.data);
    }
  }, []);

  const login = useCallback(
    async (data: UserLogin) => {
      const res = await apiLogin({ body: data });
      if (res.status === 200 && res.data?.access_token) {
        const t = res.data.access_token;
        setToken(t);
        await fetchMe(t);
      }
      return res;
    },
    [fetchMe]
  );

  const refresh = useCallback(async () => {
    const res = await refreshToken({});
    if (res.status === 200 && res.data?.access_token) {
      const t = res.data.access_token;
      setToken(t);
      await fetchMe(t);
    } else {
      setUser(undefined);
      setToken(undefined);
    }
    return res;
  }, [fetchMe]);

  const logout = useCallback(async () => {
    try {
      const res = await apiLogout(
        token ? { headers: { Authorization: `Bearer ${token}` } } : {}
      );
      return res;
    } finally {
      setUser(undefined);
      setToken(undefined);
    }
  }, [token]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const value = useMemo(
    () => ({
      isAuthenticated,
      token,
      user,
      login,
      logout,
      refresh,
    }),
    [isAuthenticated, token, user, login, logout, refresh]
  );

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}

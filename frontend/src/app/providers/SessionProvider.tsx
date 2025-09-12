import { useEffect, useMemo, useState } from 'react';
import {
  refreshToken,
  getCurrentUser,
  type UserRead,
  client,
  setResponseInterceptor,
} from 'shared/api';
import { SessionContext } from 'shared/context/SessionContext';

export function SessionProvider({ children }: React.PropsWithChildren<object>) {
  const [token, setToken] = useState<string | undefined>();
  const [user, setUser] = useState<UserRead | undefined>();

  useEffect(() => {
    client.setConfig({ auth: token });
  }, [token]);

  useEffect(() => {
    refreshToken({}).then((response) => {
      if (response.status === 200) {
        setToken(response.data?.access_token);
      }
    });
  }, []);

  useEffect(() => {
    if (!token) {
      setUser(undefined);
      return;
    }
    if (token && !user) {
      getCurrentUser().then((response) => {
        if (response.status === 200) {
          setUser(response.data);
        }
      });
    }
  }, [token, user]);

  useEffect(() => {
    const responseIntId = setResponseInterceptor(setToken);
    return () => {
      client.instance.interceptors.response.eject(responseIntId);
    };
  }, []);
  const value = useMemo(() => {
    return {
      user,
      token,
      setToken,
      setUser,
    };
  }, [user, token, setToken, setUser]);
  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}

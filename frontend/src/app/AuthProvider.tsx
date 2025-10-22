import React from 'react';
import type { UserRead } from 'shared/api/gen';
import { client } from 'shared/api/gen/client.gen';
import { getCurrentUser, refreshToken } from 'shared/api/gen/sdk.gen';
import { setResponseInterceptor } from 'shared/api/set_interceptors';
import { AuthContext, type AuthContextType } from 'shared/context/AuthContext';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<UserRead | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);

  const authenticateUser = React.useCallback(async (access_token: string) => {
    client.setConfig({ auth: access_token });
    await getCurrentUser<true>({})
      .then(({ data }) => {
        setUser(data);
      })
      .catch(() => {
        client.setConfig({ auth: undefined });
        setUser(null);
      });
  }, []);

  React.useEffect(() => {
    setIsLoading(true);
    refreshToken<true>({})
      .then(async ({ data: { access_token } }) => {
        await authenticateUser(access_token);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [authenticateUser]);

  React.useEffect(() => {
    if (!user) return;
    const responseIntId = setResponseInterceptor();
    return () => client.instance.interceptors.response.eject(responseIntId);
  }, [user]);

  if (isLoading) return <SuspenseFallback />;
  const value: AuthContextType = user
    ? { user, isAuthenticated: true, setUser }
    : { user: null, isAuthenticated: false, setUser };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

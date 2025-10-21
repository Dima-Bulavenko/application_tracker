import { getCurrentUser, login, logout, type UserLogin } from 'shared/api/gen';
import { client } from 'shared/api/gen/client.gen';
import { useAuth } from 'shared/hooks/useAuth';

export function useLogin() {
  const { setUser } = useAuth();

  return async (data: UserLogin) => {
    return login<true>({ body: data }).then(async ({ data }) => {
      client.setConfig({ auth: data.access_token });
      try {
        const { data: user } = await getCurrentUser<true>();
        setUser(user);
        return data;
      } catch (err) {
        client.setConfig({ auth: undefined });
        setUser(null);
        throw err;
      }
    });
  };
}

export function useLogout() {
  const { setUser } = useAuth();
  return async () => {
    return logout<true>({}).then(() => {
      client.setConfig({ auth: undefined });
      setUser(null);
    });
  };
}

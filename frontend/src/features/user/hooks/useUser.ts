import { getCurrentUser, login, type UserLogin } from 'shared/api/gen';
import { client } from 'shared/api/gen/client.gen';
import { useAuth } from 'shared/hooks/useAuth';

export function useLogin() {
  const { setUser } = useAuth();

  return async (data: UserLogin) => {
    login<true>({ body: data }).then(({ data: { access_token } }) => {
      client.setConfig({ auth: access_token });
      getCurrentUser<true>()
        .then(({ data }) => setUser(data))
        .catch((err) => {
          client.setConfig({ auth: undefined });
          setUser(null);
          throw err;
        });
    });
  };
}

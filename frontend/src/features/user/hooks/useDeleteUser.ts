import { deleteUser } from 'shared/api/gen';
import { client } from 'shared/api/gen/client.gen';
import { useAuth } from 'shared/hooks/useAuth';

export function useDeleteUser() {
  const { setUser } = useAuth();

  return async () => {
    return deleteUser<true>({}).then(() => {
      client.setConfig({ auth: undefined });
      setUser(null);
    });
  };
}

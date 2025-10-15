import { useNavigate } from 'react-router-dom';
import { logout } from 'shared/api/gen/sdk.gen';
import { useSession } from './useSession';

export function useLogout(redirectTo: string = '/') {
  const { setToken, setUser } = useSession();
  const navigate = useNavigate();
  const handleLogout = () => {
    logout({}).then((response) => {
      setToken(undefined);
      setUser(undefined);
      navigate(redirectTo);
      if (response.status !== 204) {
        throw Error('The logout endpoint must return status 204');
      }
    });
  };
  return handleLogout;
}

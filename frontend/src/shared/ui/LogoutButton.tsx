import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { logout } from 'shared/api';
import { useSession } from 'shared/hooks';

export function LogoutButton() {
  const { setToken, setUser } = useSession();
  const navigate = useNavigate();
  const handleLogout = () => {
    logout({}).then((response) => {
      setToken(undefined);
      setUser(undefined);
      navigate('/');
      if (response.status !== 204) {
        throw Error('The logout endpoint must return status 204');
      }
    });
  };
  return (
    <Button size='small' variant='outlined' onClick={handleLogout}>
      Logout
    </Button>
  );
}

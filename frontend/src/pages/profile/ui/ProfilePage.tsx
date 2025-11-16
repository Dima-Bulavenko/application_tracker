import { UpdateForm } from 'features/user/ui/UpdateForm';
import { DeleteAccountButton } from 'features/user/ui/DeleteAccountButton';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';

export function ProfilePage() {
  return (
    <Stack spacing={4}>
      <UpdateForm />
      <Divider />
      <DeleteAccountButton />
    </Stack>
  );
}

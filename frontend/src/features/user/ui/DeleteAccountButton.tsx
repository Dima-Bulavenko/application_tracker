import { useState } from 'react';
import DeleteIcon from '@mui/icons-material/Delete';
import { DeleteAccountDialog } from './DeleteAccountDialog';
import { useDeleteUser } from '../hooks/useDeleteUser';
import { getRouteApi } from '@tanstack/react-router';
import SubmitButton from 'shared/ui/SubmitButton';

const routeApi = getRouteApi('__root__');

export function DeleteAccountButton() {
  const [open, setOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const deleteUser = useDeleteUser();
  const navigate = routeApi.useNavigate();

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    if (!isDeleting) setOpen(false);
  };

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      await deleteUser();
      navigate({ to: '/' });
    } catch (error) {
      console.error('Failed to delete account:', error);
    } finally {
      setIsDeleting(false);
      handleClose();
    }
  };

  return (
    <>
      <SubmitButton
        variant='outlined'
        color='error'
        startIcon={<DeleteIcon />}
        isSubmitting={isDeleting}
        disabled={isDeleting}
        sx={null}
        onClick={handleOpen}>
        Delete Account
      </SubmitButton>
      <DeleteAccountDialog
        open={open}
        onClose={handleClose}
        onConfirm={handleConfirm}
        isDeleting={isDeleting}
      />
    </>
  );
}

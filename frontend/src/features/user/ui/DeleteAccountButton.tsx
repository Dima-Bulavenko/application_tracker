import { useState } from 'react';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import { DeleteAccountDialog } from './DeleteAccountDialog';
import { useDeleteUser } from '../hooks/useDeleteUser';
import { getRouteApi } from '@tanstack/react-router';

const routeApi = getRouteApi('__root__');

export function DeleteAccountButton() {
  const [open, setOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const deleteUser = useDeleteUser();
  const navigate = routeApi.useNavigate();

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      await deleteUser();
      handleClose();
      navigate({ to: '/' });
    } catch (error) {
      console.error('Failed to delete account:', error);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <>
      <Button
        variant='outlined'
        color='error'
        startIcon={<DeleteIcon />}
        onClick={handleOpen}
        sx={{ mt: 3 }}>
        Delete Account
      </Button>
      <DeleteAccountDialog
        open={open}
        onClose={handleClose}
        onConfirm={handleConfirm}
        isDeleting={isDeleting}
      />
    </>
  );
}

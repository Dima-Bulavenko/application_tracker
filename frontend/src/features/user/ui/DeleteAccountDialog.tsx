import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import SubmitButton from 'shared/ui/SubmitButton';

interface DeleteAccountDialogProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isDeleting: boolean;
}

export function DeleteAccountDialog({
  open,
  onClose,
  onConfirm,
  isDeleting,
}: DeleteAccountDialogProps) {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      aria-labelledby='delete-account-dialog-title'
      aria-describedby='delete-account-dialog-description'>
      <DialogTitle id='delete-account-dialog-title'>Delete Account</DialogTitle>
      <DialogContent>
        <DialogContentText id='delete-account-dialog-description'>
          Are you sure you want to delete your account? This action is permanent
          and cannot be undone. All your data will be permanently removed.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={isDeleting}>
          Cancel
        </Button>
        <SubmitButton
          onClick={onConfirm}
          color='error'
          variant='outlined'
          disabled={isDeleting}
          isSubmitting={isDeleting}
          sx={null}
          autoFocus>
          Delete Account
        </SubmitButton>
      </DialogActions>
    </Dialog>
  );
}

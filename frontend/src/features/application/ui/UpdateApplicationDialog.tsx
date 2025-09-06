import { Dialog, DialogTitle, DialogContent } from '@mui/material';
import UpdateApplicationForm from './UpdateApplicationForm';

type UpdateApplicationDialogProps = {
  open: boolean;
  onClose: () => void;
  application: Parameters<typeof UpdateApplicationForm>[0];
};

export function UpdateApplicationDialog({
  open,
  onClose,
  application,
}: UpdateApplicationDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='md'>
      <DialogTitle>Update Application</DialogTitle>
      <DialogContent>
        <UpdateApplicationForm {...application} />
      </DialogContent>
    </Dialog>
  );
}

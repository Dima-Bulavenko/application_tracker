import { Dialog, DialogTitle, DialogContent } from '@mui/material';
import type { ReactNode } from 'react';
import CreateApplicationForm from './CreateApplicationForm';

type CreateApplicationDialogProps = {
  open: boolean;
  onClose: () => void;
  title?: ReactNode;
};

export function CreateApplicationDialog({
  open,
  onClose,
  title = 'Create Application',
}: CreateApplicationDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='md'>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <CreateApplicationForm />
      </DialogContent>
    </Dialog>
  );
}

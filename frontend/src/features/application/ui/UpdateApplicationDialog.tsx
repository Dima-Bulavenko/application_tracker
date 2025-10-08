import { Dialog, DialogTitle, DialogContent } from '@mui/material';
import { Suspense } from 'react';
import { lazyImport } from 'shared/lib';
import type { ApplicationRead } from 'shared/api';

type UpdateApplicationDialogProps = {
  open: boolean;
  onClose: () => void;
  application: ApplicationRead;
};

const { UpdateApplicationForm } = lazyImport(
  () => import('./UpdateApplicationForm'),
  'UpdateApplicationForm'
);

export function UpdateApplicationDialog({
  open,
  onClose,
  application,
}: UpdateApplicationDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='md'>
      <DialogTitle>Update Application</DialogTitle>
      <DialogContent>
        <Suspense fallback={<div>Loading...</div>}>
          {open && <UpdateApplicationForm {...application} />}
        </Suspense>
      </DialogContent>
    </Dialog>
  );
}

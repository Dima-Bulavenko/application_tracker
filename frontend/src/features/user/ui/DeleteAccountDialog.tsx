import { Button } from 'app/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from 'app/components/ui/dialog'
import { Loader2 } from 'lucide-react'

interface DeleteAccountDialogProps {
  open: boolean
  onClose: () => void
  onConfirm: () => void
  isDeleting: boolean
}

export function DeleteAccountDialog({
  open,
  onClose,
  onConfirm,
  isDeleting,
}: DeleteAccountDialogProps) {
  return (
    <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Account</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete your account? This action is
            permanent and cannot be undone. All your data will be permanently
            removed.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant='outline' onClick={onClose} disabled={isDeleting}>
            Cancel
          </Button>
          <Button
            variant='destructive'
            onClick={onConfirm}
            disabled={isDeleting}
            autoFocus
          >
            {isDeleting ? <Loader2 className='size-4 animate-spin' /> : null}
            Delete Account
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

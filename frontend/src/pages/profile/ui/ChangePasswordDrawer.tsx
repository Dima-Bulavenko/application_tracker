import { Separator } from 'app/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { ChangePasswordForm } from 'features/user/ui/ChangePasswordForm'
import { Suspense } from 'react'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

interface ChangePasswordProps {
  open: boolean
  onClose: () => void
}

export function ChangePasswordDrawer({ open, onClose }: ChangePasswordProps) {
  return (
    <Sheet open={open} onOpenChange={(v) => !v && onClose()}>
      <SheetContent className='w-[85vw] overflow-y-auto sm:max-w-[500px]'>
        <SheetHeader>
          <SheetTitle>Change Password</SheetTitle>
        </SheetHeader>
        <Separator />
        <Suspense fallback={<SuspenseFallback />}>
          {open && <ChangePasswordForm onSuccess={onClose} />}
        </Suspense>
      </SheetContent>
    </Sheet>
  )
}

import { Separator } from 'app/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { UpdateForm } from 'features/user/ui/UpdateForm'
import { Suspense } from 'react'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

interface EditDrawerProps {
  open: boolean
  onClose: () => void
}

export function EditDrawer({ open, onClose }: EditDrawerProps) {
  return (
    <Sheet open={open} onOpenChange={(v) => !v && onClose()}>
      <SheetContent className='w-[85vw] overflow-y-auto sm:max-w-[500px]'>
        <SheetHeader>
          <SheetTitle>Edit Personal Information</SheetTitle>
        </SheetHeader>
        <Separator />
        <Suspense fallback={<SuspenseFallback />}>
          {open && <UpdateForm onSuccess={onClose} />}
        </Suspense>
      </SheetContent>
    </Sheet>
  )
}

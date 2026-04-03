import { Button } from 'app/components/ui/button'
import { Separator } from 'app/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { Pencil } from 'lucide-react'
import { Suspense, useState } from 'react'
import type { ApplicationReadWithCompany } from 'shared/api/gen/types.gen'
import { lazyImport } from 'shared/lib/lazyLoad'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

type UpdateApplicationProps = {
  application: ApplicationReadWithCompany
  open?: boolean
  onOpenChange?: (open: boolean) => void
}

const { UpdateApplicationForm } = lazyImport(
  () => import('./UpdateApplicationForm'),
  'UpdateApplicationForm'
)

export function UpdateApplication({
  application,
  open: controlledOpen,
  onOpenChange: controlledOnOpenChange,
}: UpdateApplicationProps) {
  const [internalOpen, setInternalOpen] = useState(false)

  const isControlled = controlledOpen !== undefined
  const open = isControlled ? controlledOpen : internalOpen
  const setOpen = (value: boolean) => {
    if (isControlled) {
      controlledOnOpenChange?.(value)
    } else {
      setInternalOpen(value)
    }
  }

  return (
    <>
      {!isControlled && (
        <Button onClick={() => setOpen(true)}>
          <Pencil className='size-4' />
          Edit
        </Button>
      )}
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetContent className='w-[85vw] overflow-y-auto sm:max-w-150'>
          <SheetHeader>
            <SheetTitle>Update Application</SheetTitle>
            <SheetDescription>
              Make changes to your application details with
            </SheetDescription>
          </SheetHeader>
          <Separator />
          <Suspense fallback={<SuspenseFallback />}>
            {open && <UpdateApplicationForm {...application} />}
          </Suspense>
        </SheetContent>
      </Sheet>
    </>
  )
}

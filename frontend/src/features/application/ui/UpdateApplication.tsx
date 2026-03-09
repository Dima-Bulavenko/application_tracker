import { Button } from 'app/components/ui/button'
import { Separator } from 'app/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { Pencil } from 'lucide-react'
import { Suspense, useState } from 'react'
import type { ApplicationRead } from 'shared/api/gen/types.gen'
import { lazyImport } from 'shared/lib/lazyLoad'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

type UpdateApplicationProps = {
  application: ApplicationRead
}

const { UpdateApplicationForm } = lazyImport(
  () => import('./UpdateApplicationForm'),
  'UpdateApplicationForm'
)

export function UpdateApplication({ application }: UpdateApplicationProps) {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Button onClick={() => setOpen(true)}>
        <Pencil className='size-4' />
        Edit
      </Button>
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetContent className='w-[85vw] overflow-y-auto sm:max-w-[600px]'>
          <SheetHeader>
            <SheetTitle>Update Application</SheetTitle>
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

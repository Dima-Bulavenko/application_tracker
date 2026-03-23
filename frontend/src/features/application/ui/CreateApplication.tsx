import { Button } from 'app/components/ui/button'
import { Separator } from 'app/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { Plus } from 'lucide-react'
import { Suspense, useState } from 'react'
import { lazyImport } from 'shared/lib/lazyLoad'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

const { CreateApplicationForm } = lazyImport(
  () => import('./CreateApplicationForm'),
  'CreateApplicationForm'
)

export function CreateApplication() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Button
        size='icon'
        className='fixed bottom-24 right-4 z-40'
        onClick={() => setOpen(true)}
      >
        <Plus className='size-5' />
      </Button>
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetContent className='w-[85vw] overflow-y-auto sm:max-w-[600px]'>
          <SheetHeader>
            <SheetTitle>Create Application</SheetTitle>
            <SheetDescription>
              Add a new job application to track
            </SheetDescription>
          </SheetHeader>
          <Separator />
          <Suspense fallback={<SuspenseFallback />}>
            {open && <CreateApplicationForm onSuccess={() => setOpen(false)} />}
          </Suspense>
        </SheetContent>
      </Sheet>
    </>
  )
}

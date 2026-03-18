import { Button } from 'app/components/ui/button'
import { Sheet, SheetContent } from 'app/components/ui/sheet'
import { Filter } from 'lucide-react'
import { Suspense, useState } from 'react'

import { lazyImport } from 'shared/lib/lazyLoad'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

const { FilterApplicationForm } = lazyImport(
  () => import('./FilterApplicationForm'),
  'FilterApplicationForm'
)

export function FilterApplication() {
  const [open, setOpen] = useState(false)
  const filterPanel = (
    <Suspense fallback={<SuspenseFallback />}>
      <FilterApplicationForm />
    </Suspense>
  )

  return (
    <>
      {/* Mobile: button + sheet */}
      <div className='md:hidden'>
        <Button
          size='icon'
          className='fixed bottom-4 right-4 z-40'
          onClick={() => setOpen(true)}
        >
          <Filter className='size-5' />
        </Button>
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetContent className='w-[85vw] max-w-[420px] overflow-y-auto'>
            {open && filterPanel}
          </SheetContent>
        </Sheet>
      </div>

      {/* Desktop: sticky sidebar */}
      <div className='hidden md:sticky md:top-4 md:block'>{filterPanel}</div>
    </>
  )
}

import { Button } from 'app/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { Filter } from 'lucide-react'
import { Suspense, useState } from 'react'
import { useMediaQuery } from 'shared/hooks/useMediaQuery'
import { lazyImport } from 'shared/lib/lazyLoad'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

const { FilterApplicationForm } = lazyImport(
  () => import('./FilterApplicationForm'),
  'FilterApplicationForm'
)

export function FilterApplication() {
  const [open, setOpen] = useState(false)
  const isDesktop = useMediaQuery('(min-width: 768px)')
  const filterPanel = (
    <Suspense fallback={<SuspenseFallback />}>
      <FilterApplicationForm />
    </Suspense>
  )

  if (isDesktop) {
    return <div className='md:sticky md:top-4'>{filterPanel}</div>
  }

  return (
    <div>
      <Button
        size='icon'
        className='fixed bottom-4 right-4 z-40'
        onClick={() => setOpen(true)}
      >
        <Filter className='size-5' />
      </Button>
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetContent className='w-[85vw] max-w-105 overflow-y-auto'>
          <SheetHeader>
            <SheetTitle>Filter Applications</SheetTitle>
            <SheetDescription>
              Narrow down your applications by filters
            </SheetDescription>
          </SheetHeader>
          {open && filterPanel}
        </SheetContent>
      </Sheet>
    </div>
  )
}

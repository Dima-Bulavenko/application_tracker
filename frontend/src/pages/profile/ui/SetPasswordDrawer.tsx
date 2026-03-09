import { getRouteApi } from '@tanstack/react-router'
import { Separator } from 'app/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from 'app/components/ui/sheet'
import { Suspense } from 'react'
import { getCurrentUser } from 'shared/api/gen'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'
import { SetPasswordForm } from './SetPasswordForm'

interface SetPasswordProps {
  open: boolean
  onClose: () => void
}

const routeApi = getRouteApi('/_authenticated')

export function SetPasswordDrawer({ open, onClose }: SetPasswordProps) {
  const {
    auth: { setUser },
  } = routeApi.useRouteContext()
  const onSuccess = async () => {
    const { data } = await getCurrentUser()
    setUser(data)
    onClose()
  }

  return (
    <Sheet open={open} onOpenChange={(v) => !v && onClose()}>
      <SheetContent className='w-[85vw] overflow-y-auto sm:max-w-[500px]'>
        <SheetHeader>
          <SheetTitle>Set Password</SheetTitle>
        </SheetHeader>
        <Separator />
        <Suspense fallback={<SuspenseFallback />}>
          {open && <SetPasswordForm onSuccess={onSuccess} />}
        </Suspense>
      </SheetContent>
    </Sheet>
  )
}

import { Loader2 } from 'lucide-react'

export function SuspenseFallback() {
  return (
    <div className='flex min-h-[200px] w-full items-center justify-center'>
      <Loader2 className='size-8 animate-spin text-muted-foreground' />
    </div>
  )
}

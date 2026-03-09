import { Card, CardContent, CardHeader } from 'app/components/ui/card'
import { Separator } from 'app/components/ui/separator'
import { Skeleton } from 'app/components/ui/skeleton'

export function ApplicationCardSkeleton() {
  return (
    <Card className='max-w-[720px]'>
      <CardHeader>
        <Skeleton className='h-8 w-3/5' />
        <Skeleton className='h-5 w-2/5' />
      </CardHeader>
      <CardContent className='space-y-3'>
        <div className='flex flex-wrap gap-2'>
          <Skeleton className='h-6 w-[90px] rounded-full' />
          <Skeleton className='h-6 w-[80px] rounded-full' />
          <Skeleton className='h-6 w-[75px] rounded-full' />
          <Skeleton className='h-6 w-[120px] rounded-full' />
        </div>

        <Separator />

        <div className='flex gap-3'>
          <Skeleton className='h-4 w-[150px]' />
          <Skeleton className='h-4 w-[150px]' />
        </div>

        <div className='flex gap-2'>
          <Skeleton className='h-9 w-[100px] rounded-md' />
          <Skeleton className='h-9 w-14 rounded-md' />
        </div>
      </CardContent>
    </Card>
  )
}

export default ApplicationCardSkeleton

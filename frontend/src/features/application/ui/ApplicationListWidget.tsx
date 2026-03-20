import { ApplicationList } from 'entities/application/ui/ApplicationList'
import { ApplicationListSkeleton } from 'entities/application/ui/ApplicationListSkeleton'
import { Suspense } from 'react'
import { FilterApplication } from './FilterApplication'

export function ApplicationListWidget() {
  return (
    <div className='grid w-full items-start gap-4 md:grid-cols-[1fr_360px]'>
      <Suspense fallback={<ApplicationListSkeleton />}>
        <ApplicationList />
      </Suspense>
      <FilterApplication />
    </div>
  )
}

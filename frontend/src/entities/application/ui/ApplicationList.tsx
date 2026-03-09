import { useSuspenseQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { applicationsOptions } from 'entities/application/api/queryOptions'
import ApplicationCard from './ApplicationCard'
import ApplicationCardSkeleton from './ApplicationCardSkeleton'

const routeApi = getRouteApi('/_authenticated/dashboard')

export function ApplicationList() {
  const { filter } = routeApi.useSearch()
  const { error, isFetching, data } = useSuspenseQuery(
    applicationsOptions(filter)
  )

  if (error) {
    return (
      <div className='flex flex-col items-center gap-2'>
        <p className='text-sm text-destructive'>{error.message}</p>
      </div>
    )
  }

  if (!isFetching && data?.length === 0) {
    return <p className='text-sm text-muted-foreground'>No applications yet.</p>
  }

  if (isFetching) {
    return (
      <div className='space-y-4'>
        {Array.from({ length: 5 }).map((_, index) => (
          <ApplicationCardSkeleton key={index} />
        ))}
      </div>
    )
  }

  return (
    <div className='space-y-4'>
      {data?.map((app) => (
        <ApplicationCard key={app.id} application={app} />
      ))}
    </div>
  )
}

export default ApplicationList

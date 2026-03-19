import { useSuspenseQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { applicationsOptions } from 'entities/application/api/queryOptions'
import { getPaginationPrams } from 'shared/lib/getPaginationPrams'
import ApplicationCard from './ApplicationCard'

const routeApi = getRouteApi('/_authenticated/dashboard')

export function ApplicationList() {
  const { filter, page } = routeApi.useSearch()
  const {
    error,
    data: { items },
  } = useSuspenseQuery(
    applicationsOptions({ ...filter, ...getPaginationPrams(page) })
  )

  if (error) {
    return (
      <div className='flex flex-col items-center gap-2'>
        <p className='text-sm text-destructive'>{error.message}</p>
      </div>
    )
  }

  if (items?.length === 0) {
    return <p className='text-sm text-muted-foreground'>No applications yet.</p>
  }

  return (
    <div className='space-y-4'>
      {items?.map((app) => (
        <ApplicationCard key={app.id} application={app} />
      ))}
    </div>
  )
}

export default ApplicationList

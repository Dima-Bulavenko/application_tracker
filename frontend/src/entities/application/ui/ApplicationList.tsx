import { useSuspenseQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { applicationsOptions } from 'entities/application/api/queryOptions'
import { getPaginationPrams } from 'shared/lib/getPaginationPrams'
import { PaginationControls } from 'shared/ui/PaginationControls'
import ApplicationCard from './ApplicationCard'

const routeApi = getRouteApi('/_authenticated/dashboard')

export function ApplicationList() {
  const { filter, page } = routeApi.useSearch()
  const navigate = routeApi.useNavigate()
  const {
    error,
    data: { items, total, limit },
  } = useSuspenseQuery(
    applicationsOptions({ ...filter, ...getPaginationPrams(page) })
  )

  const totalPages = Math.max(1, Math.ceil(total / limit))
  const currentPage = Math.min(page, totalPages)

  const handlePageChange = (nextPage: number) => {
    navigate({ search: (prev) => ({ ...prev, page: nextPage }) })
  }

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
      {items.map((app) => (
        <ApplicationCard key={app.id} application={app} />
      ))}

      <PaginationControls
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
      />
    </div>
  )
}

export default ApplicationList

import { createFileRoute, stripSearchParams } from '@tanstack/react-router'
import { applicationsOptions } from 'entities/application/api/queryOptions'
import {
  defaultFilters,
  zApplicationFilterSchema,
} from 'features/application/model/filterSchema'
import { DashboardPage } from 'pages/dashboard/ui/DashboardPage'
import { getPaginationPrams } from 'shared/lib/getPaginationPrams'
import z from 'zod'

const af = zApplicationFilterSchema.shape

export const ApplicationFilterSearchSchema = z.object({
  order_by: af.order_by.optional().catch(undefined),
  order_direction: af.order_direction.optional().catch(undefined),
  status: af.status.min(1).optional().catch(undefined),
  work_type: af.work_type.min(1).optional().catch(undefined),
  work_location: af.work_location.min(1).optional().catch(undefined),
  role_name: af.role_name.min(1).optional().catch(undefined),
  company_name: af.company_name.min(1).optional().catch(undefined),
})

export const DashboardSearchSchema = z.object({
  filter: ApplicationFilterSearchSchema.optional().catch(undefined),
  page: z.int().gte(1).positive().default(1).catch(1),
})

export const Route = createFileRoute('/_authenticated/dashboard')({
  validateSearch: DashboardSearchSchema,
  search: {
    middlewares: [
      stripSearchParams({
        filter: {
          order_by: defaultFilters.order_by,
          order_direction: defaultFilters.order_direction,
        },
        page: 1,
      }),
    ],
  },
  loaderDeps: ({ search: { page, filter } }) => ({ filter, page }),
  loader: ({ context: { queryClient }, deps: { filter, page } }) => {
    queryClient.ensureQueryData(
      applicationsOptions({
        ...filter,
        ...getPaginationPrams(page),
      })
    )
  },
  component: DashboardPage,
})

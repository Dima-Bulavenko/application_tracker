import {
  zApplicationOrderBy,
  zAppStatus,
  zWorkLocation,
  zWorkType,
} from 'shared/api/gen/zod.gen'
import z from 'zod'

export const zApplicationFilterSchema = z.object({
  order_by: zApplicationOrderBy,
  order_direction: z.enum(['asc', 'desc']),
  status: z.array(zAppStatus),
  work_type: z.array(zWorkType),
  work_location: z.array(zWorkLocation),
  role_name: z.string().max(40, 'Role name must be at most 40 characters'),
  company_name: z
    .string()
    .max(40, 'Company name must be at most 40 characters'),
})

export type ApplicationFilter = z.infer<typeof zApplicationFilterSchema>

export const defaultFilters: ApplicationFilter = {
  company_name: '',
  status: [],
  work_location: [],
  work_type: [],
  order_by: 'time_create',
  order_direction: 'desc',
  role_name: '',
}

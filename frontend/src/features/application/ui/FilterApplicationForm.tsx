import { zodResolver } from '@hookform/resolvers/zod'

import {
  keepPreviousData,
  useIsFetching,
  useQuery,
} from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { Button } from 'app/components/ui/button'
import { FieldGroup } from 'app/components/ui/field'
import {
  applicationKeys,
  userCompaniesOptions,
} from 'entities/application/api/queryOptions'
import { Loader2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { type Control, useController, useForm } from 'react-hook-form'
import {
  zApplicationOrderBy,
  zAppStatus,
  zWorkLocation,
  zWorkType,
} from 'shared/api/gen/zod.gen'
import { FormField } from 'shared/ui/FormField'
import {
  AsyncSelectInput,
  SelectInput,
  SelectMultipleInput,
} from 'shared/ui/SelectInput'
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

type ApplicationFilter = z.infer<typeof zApplicationFilterSchema>

type FilterFormParam = {
  control: Control<ApplicationFilter>
}

const routeApi = getRouteApi('/_authenticated/dashboard')

function OrderBy({ control }: FilterFormParam) {
  const controller = useController<ApplicationFilter, 'order_by'>({
    name: 'order_by',
    control,
  })
  const id = `${controller.field.name}_id`
  const options = zApplicationOrderBy.options
  return (
    <FormField controller={controller} htmlFor={id} label='Order By'>
      <SelectInput controller={controller} id={id} options={options} />
    </FormField>
  )
}

function OrderDirection({ control }: FilterFormParam) {
  const controller = useController<ApplicationFilter, 'order_direction'>({
    name: 'order_direction',
    control,
  })
  const id = `${controller.field.name}_id`
  return (
    <FormField controller={controller} htmlFor={id} label='Order Direction'>
      <SelectInput controller={controller} id={id} options={['asc', 'desc']} />
    </FormField>
  )
}

function ApplicationStatusFilter({ control }: FilterFormParam) {
  const options = zAppStatus.options
  const controller = useController({
    name: 'status',
    control,
  })
  const id = `${controller.field.name}_id`
  return (
    <FormField controller={controller} htmlFor={id} label='Application Status'>
      <SelectMultipleInput
        id={id}
        controller={controller}
        options={options}
        placeholder='Select Status'
      />
    </FormField>
  )
}

function WorkLocationFilter({ control }: FilterFormParam) {
  const options = zWorkLocation.options
  const controller = useController({
    name: 'work_location',
    control,
  })
  const id = `${controller.field.name}_id`
  return (
    <FormField controller={controller} htmlFor={id} label='Work Location'>
      <SelectMultipleInput
        id={id}
        controller={controller}
        options={options}
        placeholder='Select Work Locations'
      />
    </FormField>
  )
}

function WorkTypeFilter({ control }: FilterFormParam) {
  const options = zWorkType.options
  const controller = useController({
    name: 'work_type',
    control,
  })
  const id = `${controller.field.name}_id`
  return (
    <FormField controller={controller} htmlFor={id} label='Work Type'>
      <SelectMultipleInput
        id={id}
        controller={controller}
        options={options}
        placeholder='Select Work Types'
      />
    </FormField>
  )
}

function CompanyNameFilter({ control }: FilterFormParam) {
  const controller = useController<ApplicationFilter, 'company_name'>({
    name: 'company_name',
    control,
  })
  const [open, setOpen] = useState(false)
  const { data = [], isFetching } = useQuery({
    ...userCompaniesOptions({
      name_contains: controller.field.value,
      limit: 30,
    }),
    select: (data) => data.map((company) => company.name),
    enabled: open,
    placeholderData: keepPreviousData,
  })
  const id = `${controller.field.name}_id`
  return (
    <FormField controller={controller} htmlFor={id} label='Company Name'>
      <AsyncSelectInput
        controller={controller}
        id={id}
        options={data}
        placeholder='Select Company'
        isFetching={isFetching}
        open={open}
        setOpen={setOpen}
      />
    </FormField>
  )
}

export const defaultFilters: ApplicationFilter = {
  company_name: '',
  status: [],
  work_location: [],
  work_type: [],
  order_by: 'time_create',
  order_direction: 'desc',
  role_name: '',
}

export function FilterApplicationForm() {
  const { filter } = routeApi.useSearch()
  const navigate = routeApi.useNavigate()
  const {
    control,
    handleSubmit,
    formState: { isDirty },
    reset,
  } = useForm<ApplicationFilter>({
    resolver: zodResolver(zApplicationFilterSchema),
    defaultValues: {
      ...defaultFilters,
      ...filter,
    },
  })
  const isFetching = useIsFetching({ queryKey: applicationKeys.lists() })
  const hasAppliedFilters = Boolean(filter && Object.keys(filter).length > 0)

  useEffect(() => {
    reset({ ...defaultFilters, ...filter })
  }, [filter, reset])

  const clearFilters = () => {
    if (filter) {
      navigate({ search: ({ filter, ...rest }) => ({ ...rest }) })
      return
    }

    reset(defaultFilters)
  }

  return (
    <div className='space-y-6 p-4'>
      <ApplicationStatusFilter control={control} />
      <WorkTypeFilter control={control} />
      <CompanyNameFilter control={control} />
      <WorkLocationFilter control={control} />
      <FieldGroup className='grid max-w-sm grid-cols-2'>
        <OrderBy control={control} />
        <OrderDirection control={control} />
      </FieldGroup>
      <div className='flex justify-end gap-2'>
        <Button
          disabled={!isDirty && !hasAppliedFilters}
          onClick={clearFilters}
          type='button'
          variant='outline'
        >
          Clear Filters
        </Button>
        <Button
          disabled={!isDirty}
          onClick={handleSubmit((filter) =>
            navigate({ search: (prev) => ({ ...prev, filter: filter }) })
          )}
          type='button'
        >
          {isFetching ? <Loader2 className='size-4 animate-spin' /> : null}
          Apply Filters
        </Button>
      </div>
    </div>
  )
}

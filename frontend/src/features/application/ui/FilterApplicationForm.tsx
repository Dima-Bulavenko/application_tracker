import { DevTool } from '@hookform/devtools'
import { useIsFetching } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { Button } from 'app/components/ui/button'
import { Label } from 'app/components/ui/label'
import { RadioGroup, RadioGroupItem } from 'app/components/ui/radio-group'
import { applicationKeys } from 'entities/application/api/queryOptions'
import CompanyField from 'entities/application/ui/CompanyField'
import {
  type ApplicationFilter,
  cleanFilterData,
  filterStorage,
} from 'features/application/lib/filterStorage'
import { Loader2 } from 'lucide-react'
import { type Control, useController, useForm } from 'react-hook-form'
import { zAppStatus, zWorkLocation, zWorkType } from 'shared/api/gen/zod.gen'
import { FormField } from 'shared/ui/FormField'
import { SelectMultipleInput } from 'shared/ui/SelectField'

type FilterFormParam = {
  control: Control<ApplicationFilter>
}

const routeApi = getRouteApi('/_authenticated/dashboard')

function OrderBy({ control }: FilterFormParam) {
  const { field } = useController<ApplicationFilter, 'order_by'>({
    name: 'order_by',
    control,
  })
  return (
    <fieldset className='space-y-2'>
      <Label>Order By</Label>
      <RadioGroup value={field.value ?? ''} onValueChange={field.onChange}>
        <label className='flex items-center gap-2'>
          <RadioGroupItem value='time_create' />
          <span className='text-sm'>Time Create</span>
        </label>
        <label className='flex items-center gap-2'>
          <RadioGroupItem value='time_update' />
          <span className='text-sm'>Time Update</span>
        </label>
      </RadioGroup>
    </fieldset>
  )
}

function OrderDirection({ control }: FilterFormParam) {
  const { field } = useController<ApplicationFilter, 'order_direction'>({
    name: 'order_direction',
    control,
  })
  return (
    <fieldset className='space-y-2'>
      <Label>Order Direction</Label>
      <RadioGroup value={field.value ?? ''} onValueChange={field.onChange}>
        <label className='flex items-center gap-2'>
          <RadioGroupItem value='desc' />
          <span className='text-sm'>Descending</span>
        </label>
        <label className='flex items-center gap-2'>
          <RadioGroupItem value='asc' />
          <span className='text-sm'>Ascending</span>
        </label>
      </RadioGroup>
    </fieldset>
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

export function FilterApplicationForm() {
  const { filter } = routeApi.useSearch()
  const navigate = routeApi.useNavigate()
  const { control, handleSubmit, formState, reset } =
    useForm<ApplicationFilter>({
      defaultValues: filter,
    })

  const isFetching = useIsFetching({ queryKey: applicationKeys.lists() })

  const applyFilter = (data: ApplicationFilter): void => {
    const cleanedFilters = cleanFilterData(data)
    const hasActiveFilters = Object.keys(cleanedFilters).length > 0

    filterStorage.save(cleanedFilters)
    navigate({
      search: () => (hasActiveFilters ? { filter: cleanedFilters } : {}),
    })
  }

  const clearFilters = (): void => {
    filterStorage.clear()
    reset({})
    navigate({ search: () => ({}) })
  }

  const hasActiveFilters = Boolean(filter)

  return (
    <div className='space-y-6 p-4'>
      <div className='space-y-4'>
        <OrderBy control={control} />
        <OrderDirection control={control} />
      </div>
      <ApplicationStatusFilter control={control} />
      <WorkLocationFilter control={control} />
      <WorkTypeFilter control={control} />
      <CompanyField control={control} name='company_name' />
      <div className='flex justify-end gap-2'>
        <Button
          disabled={!formState.isDirty && !hasActiveFilters}
          onClick={clearFilters}
          type='button'
          variant='outline'
        >
          Clear Filters
        </Button>
        <Button
          disabled={!formState.isDirty}
          onClick={handleSubmit(applyFilter)}
          type='button'
        >
          {isFetching ? <Loader2 className='size-4 animate-spin' /> : null}
          Apply Filters
        </Button>
      </div>
      <DevTool control={control} placement='bottom-left' />
    </div>
  )
}

import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { FieldPath, FieldValues, useController } from 'react-hook-form'
import { getUserCompanies } from 'shared/api/gen/sdk.gen'
import type { BaseFormFiledProps } from 'shared/types/form'
import { FormField } from 'shared/ui/FormField'
import { AsyncSelectInput } from 'shared/ui/SelectInput'

export default function CompanyField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
  TTransformedValues = V,
>({
  label = 'Company',
  description,
  ...props
}: BaseFormFiledProps<V, N, TTransformedValues>) {
  const controller = useController({ ...props })
  const [open, setOpen] = useState(false)
  const { field } = controller
  const id = `${controller.field.name}_id`

  const { data, isFetching } = useQuery({
    queryKey: ['companies', field.value],
    queryFn: async ({ queryKey }) => {
      const response = await getUserCompanies<true>({
        query: { limit: 30, name_contains: queryKey[1] },
      })
      return response.data
    },
    placeholderData: keepPreviousData,
    enabled: open,
    staleTime: Infinity,
    select: (data) => data.map((company) => company.name),
  })

  return (
    <FormField
      controller={controller}
      htmlFor={id}
      label={label}
      description={description}
    >
      <AsyncSelectInput
        setOpen={setOpen}
        open={open}
        isFetching={isFetching}
        controller={controller}
        options={data ?? []}
        id={id}
      />
    </FormField>
  )
}

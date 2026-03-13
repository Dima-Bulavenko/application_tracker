import { useDebouncedCallback } from '@tanstack/react-pacer/debouncer'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from 'app/components/ui/combobox'
import { Spinner } from 'app/components/ui/spinner'
import { useState } from 'react'
import { useController } from 'react-hook-form'
import { getUserCompanies } from 'shared/api/gen/sdk.gen'

const CompanyField = ({ label = 'Company', ...props }) => {
  const controller = useController(props)
  const [open, setOpen] = useState(false)
  const { field, fieldState } = controller
  console.log('Field val', field.value)

  const debouncedFetching = useDebouncedCallback(field.onChange, { wait: 400 })

  const { data = [], isFetching } = useQuery({
    queryKey: ['companies', field.value],
    queryFn: async ({ queryKey }) => {
      const response = await getUserCompanies<true>({
        query: { limit: 30, name_contains: queryKey[1] },
      })
      return response.data
    },
    placeholderData: keepPreviousData,
    enabled: open,
    staleTime: 30000,
    select: (data) => data.map((company) => company.name),
  })

  return (
    <Combobox
      items={data}
      value={field.value}
      // onValueChange={field.onChange}
      open={open}
      onOpenChange={setOpen}
      onInputValueChange={debouncedFetching}
    >
      <ComboboxInput placeholder='Company Field' />
      <ComboboxContent>
        {isFetching && <Spinner className='size-7' />}
        {!isFetching && <ComboboxEmpty>No items found.</ComboboxEmpty>}
        <ComboboxList>
          {(item) => (
            <ComboboxItem key={item} value={item}>
              {item}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}

export default CompanyField

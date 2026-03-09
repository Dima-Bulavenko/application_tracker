import { useDebouncedCallback } from '@tanstack/react-pacer/debouncer'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { Input } from 'app/components/ui/input'
import { Label } from 'app/components/ui/label'
import { Loader2 } from 'lucide-react'
import React, { useRef, useState } from 'react'
import { useController } from 'react-hook-form'
import { getUserCompanies } from 'shared/api/gen/sdk.gen'
import type { FieldComponent } from 'shared/types/form'

const CompanyField: FieldComponent = ({ label = 'Company', ...props }) => {
  const controller = useController(props)
  const [open, setOpen] = useState(false)
  const { field, fieldState } = controller
  const containerRef = useRef<HTMLDivElement>(null)
  const errorMessage = fieldState?.error?.message
  const id = `${field.name}_id`

  const debouncedFetching = useDebouncedCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = e.target.value
      field.onChange(val.trim() === '' ? null : val)
    },
    { wait: 400 }
  )

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
  })

  return (
    <div className='relative space-y-2' ref={containerRef}>
      {label && <Label htmlFor={id}>{label}</Label>}
      <div className='relative'>
        <Input
          id={id}
          name={field.name}
          ref={field.ref}
          value={field.value ?? ''}
          onChange={debouncedFetching}
          onFocus={() => setOpen(true)}
          onBlur={(e) => {
            field.onBlur()
            if (!containerRef.current?.contains(e.relatedTarget)) {
              setOpen(false)
            }
          }}
          aria-invalid={!!fieldState?.error}
          autoComplete='off'
        />
        {isFetching && (
          <Loader2 className='absolute right-2 top-1/2 size-4 -translate-y-1/2 animate-spin text-muted-foreground' />
        )}
      </div>
      {open && data.length > 0 && (
        <ul className='absolute z-50 mt-1 max-h-48 w-full overflow-auto rounded-md border bg-popover p-1 shadow-md'>
          {data.map((c) => (
            <li key={c.name}>
              <button
                type='button'
                className='w-full cursor-pointer rounded-sm px-2 py-1.5 text-left text-sm hover:bg-accent'
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => {
                  field.onChange(c.name)
                  setOpen(false)
                }}
              >
                {c.name}
              </button>
            </li>
          ))}
        </ul>
      )}
      {errorMessage && (
        <p className='text-sm text-destructive'>{errorMessage}</p>
      )}
    </div>
  )
}

export default CompanyField

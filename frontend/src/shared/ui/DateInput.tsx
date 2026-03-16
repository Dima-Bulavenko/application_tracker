'use client'

import { Calendar } from 'app/components/ui/calendar'
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from 'app/components/ui/input-group'
import {
  Popover,
  PopoverAnchor,
  PopoverContent,
  PopoverTrigger,
} from 'app/components/ui/popover'
import { format } from 'date-fns'
import { CalendarIcon, XIcon } from 'lucide-react'
import * as React from 'react'
import { FieldPath, FieldValues, UseControllerReturn } from 'react-hook-form'

type DateInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = { controller: UseControllerReturn<V, N>; id: string } & Omit<
  React.ComponentProps<'input'>,
  'name' | 'value' | 'onChange' | 'id'
>

export function DateInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ controller, id, ...props }: DateInputProps<V, N>) {
  const { field, fieldState, formState } = controller
  const [open, setOpen] = React.useState(false)
  const rawValue = field.value as unknown

  const selectedDate = React.useMemo(() => {
    if (!rawValue) {
      return undefined
    }

    if (rawValue instanceof Date) {
      return rawValue
    }

    if (typeof rawValue === 'string') {
      const parsedDate = new Date(rawValue)
      return Number.isNaN(parsedDate.getTime()) ? undefined : parsedDate
    }

    return undefined
  }, [rawValue])

  const handleDateSelect = React.useCallback(
    (date?: Date) => {
      field.onChange(date ? date.toISOString() : null)
      setOpen(false)
    },
    [field]
  )

  const handleDateClear = React.useCallback(() => {
    field.onChange(null)
    field.onBlur()
    setOpen(false)
  }, [field])

  const displayValue = selectedDate ? format(selectedDate, 'dd/MM/yyyy') : ''

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverAnchor asChild>
        <InputGroup>
          <InputGroupInput
            aria-invalid={fieldState.invalid}
            disabled={formState.isSubmitting}
            name={field.name}
            id={id}
            value={displayValue}
            placeholder='Select date'
            readOnly
            onClick={() => setOpen(true)}
            onFocus={() => setOpen(true)}
            onBlur={field.onBlur}
            {...props}
          />
          <InputGroupAddon align='inline-end'>
            {selectedDate ? (
              <InputGroupButton
                variant='ghost'
                size='icon-xs'
                aria-label='Clear date'
                disabled={formState.isSubmitting}
                onClick={handleDateClear}
              >
                <XIcon />
                <span className='sr-only'>Clear date</span>
              </InputGroupButton>
            ) : null}
            <PopoverTrigger asChild>
              <InputGroupButton
                variant='ghost'
                size='icon-xs'
                aria-label='Select date'
                disabled={formState.isSubmitting}
              >
                <CalendarIcon />
                <span className='sr-only'>Select date</span>
              </InputGroupButton>
            </PopoverTrigger>
          </InputGroupAddon>
        </InputGroup>
      </PopoverAnchor>
      <PopoverContent className='w-auto overflow-hidden p-0' align='center'>
        <Calendar
          mode='single'
          selected={selectedDate}
          onSelect={handleDateSelect}
          captionLayout='dropdown'
          defaultMonth={selectedDate}
        />
      </PopoverContent>
    </Popover>
  )
}

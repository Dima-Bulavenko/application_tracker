import { Checkbox } from 'app/components/ui/checkbox'
import { Label } from 'app/components/ui/label'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from 'app/components/ui/select'
import type {
  FieldPath,
  FieldValues,
  UseControllerReturn,
} from 'react-hook-form'
import type { SelectMultipleProps } from 'shared/types/form'

const defaultHumanize = (v: string) =>
  v.charAt(0).toUpperCase() + v.slice(1).replace('_', ' ')

export type SelectInputProps<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
> = {
  label?: string
  placeholder?: string
  options: readonly string[]
  controller: UseControllerReturn<TFieldValues, TName>
  id: string
}

export function SelectInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ label, options, controller, id, placeholder }: SelectInputProps<V, N>) {
  const { field, fieldState } = controller
  return (
    <Select
      name={field.name}
      onValueChange={field.onChange}
      value={field.value}
    >
      <SelectTrigger
        id={id}
        aria-invalid={fieldState.invalid}
        className='w-full'
      >
        {placeholder ?? <SelectValue placeholder='Select a fruit' />}
      </SelectTrigger>
      <SelectContent position='popper'>
        <SelectGroup>
          {label ?? <SelectLabel>{label}</SelectLabel>}
          {options.map((option) => (
            <SelectItem key={option} value={option}>
              {defaultHumanize(option)}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}

export function MultipleSelectField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  options,
  controller,
  humanize = defaultHumanize,
  label,
  helperText,
}: SelectMultipleProps<V, N>) {
  const { field, fieldState } = controller
  const selectedValues: string[] = Array.isArray(field.value) ? field.value : []
  const errorMessage = fieldState?.error?.message

  const toggleOption = (opt: string) => {
    const next = selectedValues.includes(opt)
      ? selectedValues.filter((v) => v !== opt)
      : [...selectedValues, opt]
    field.onChange(next.length > 0 ? next : undefined)
  }

  return (
    <div className='space-y-2'>
      {label && <Label>{label}</Label>}
      <div className='space-y-1'>
        {options.map((opt) => (
          <label key={opt} className='flex items-center gap-2'>
            <Checkbox
              checked={selectedValues.includes(opt)}
              onCheckedChange={() => toggleOption(opt)}
            />
            <span className='text-sm'>{humanize(opt)}</span>
          </label>
        ))}
      </div>
      {errorMessage && (
        <p className='text-sm text-destructive'>{errorMessage}</p>
      )}
      {!errorMessage && helperText && (
        <p className='text-sm text-muted-foreground'>{helperText}</p>
      )}
    </div>
  )
}

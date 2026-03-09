import { Checkbox } from 'app/components/ui/checkbox'
import { Label } from 'app/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from 'app/components/ui/select'
import type { FieldPath, FieldValues } from 'react-hook-form'
import type { SelectInputProps, SelectMultipleProps } from 'shared/types/form'

const defaultHumanize = (v: string) =>
  v.charAt(0).toUpperCase() + v.slice(1).replace('_', ' ')

export function SelectField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  humanize = defaultHumanize,
  options,
  controller,
  label,
  helperText,
}: SelectInputProps<V, N>) {
  const { field, fieldState } = controller
  const errorMessage = fieldState?.error?.message
  const id = `${field.name}_id`

  return (
    <div className='space-y-2'>
      {label && <Label htmlFor={id}>{label}</Label>}
      <Select
        value={field.value ?? ''}
        onValueChange={(value) => field.onChange(value)}
        disabled={field.disabled}
      >
        <SelectTrigger
          id={id}
          ref={field.ref}
          onBlur={field.onBlur}
          className='w-full'
          aria-invalid={!!fieldState?.error}
        >
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {options.map((opt) => (
            <SelectItem key={opt} value={opt}>
              {humanize(opt)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {errorMessage && (
        <p className='text-sm text-destructive'>{errorMessage}</p>
      )}
      {!errorMessage && helperText && (
        <p className='text-sm text-muted-foreground'>{helperText}</p>
      )}
    </div>
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

import { Input } from 'app/components/ui/input'
import { FieldPath, FieldValues, useController } from 'react-hook-form'
import type { BaseFormFiledProps } from 'shared/types/form'
import { FormField } from 'shared/ui/FormField'

function toDatetimeLocal(iso: string | null | undefined): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const pad = (n: number) => n.toString().padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

export default function InterviewDateField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  label = 'Interview date',
  description,
  ...props
}: BaseFormFiledProps<V, N>) {
  const controller = useController({ ...props })
  const { field, fieldState } = controller
  const id = `${field.name}_id`

  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <Input
        id={id}
        type='datetime-local'
        name={field.name}
        ref={field.ref}
        value={toDatetimeLocal(field.value)}
        onBlur={field.onBlur}
        onChange={(e) => {
          const val = e.target.value
          field.onChange(val ? new Date(val).toISOString() : null)
        }}
        aria-invalid={!!fieldState.error}
      />
    </FormField>
  )
}

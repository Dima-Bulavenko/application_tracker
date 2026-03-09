import { Input } from 'app/components/ui/input'
import { Label } from 'app/components/ui/label'
import { useController } from 'react-hook-form'
import type { FieldComponent } from 'shared/types/form'

function toDatetimeLocal(iso: string | null | undefined): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const pad = (n: number) => n.toString().padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const InterviewDateField: FieldComponent = ({
  label = 'Interview date',
  ...props
}) => {
  const { field, fieldState } = useController(props)
  const errorMessage = fieldState.error?.message
  const id = `${field.name}_id`

  return (
    <div className='space-y-2'>
      <Label htmlFor={id}>{label}</Label>
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
      {errorMessage && (
        <p className='text-sm text-destructive'>{errorMessage}</p>
      )}
    </div>
  )
}

export default InterviewDateField

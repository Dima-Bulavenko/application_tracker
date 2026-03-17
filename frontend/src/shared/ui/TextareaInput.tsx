import { Label } from 'app/components/ui/label'
import { Textarea } from 'app/components/ui/textarea'
import type { FieldPath, FieldValues } from 'react-hook-form'
import type { TextareaInputProps } from 'shared/types/form'

export function TextareaInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ label, controller, helperText, ...props }: TextareaInputProps<V, N>) {
  const { field, fieldState, formState } = controller
  const errorMessage = fieldState?.error?.message
  const id = `${field.name}_id`

  return (
    <div className='space-y-2'>
      {label && <Label htmlFor={id}>{label}</Label>}
      <Textarea
        id={id}
        disabled={
          formState.isSubmitting || formState.isLoading || field.disabled
        }
        onBlur={field.onBlur}
        onChange={field.onChange}
        name={field.name}
        ref={field.ref}
        value={field.value ?? ''}
        aria-invalid={!!fieldState?.error}
        {...props}
      />
      {errorMessage && (
        <p className='text-sm text-destructive'>{errorMessage}</p>
      )}
      {!errorMessage && helperText && (
        <p className='text-sm text-muted-foreground'>{helperText}</p>
      )}
    </div>
  )
}

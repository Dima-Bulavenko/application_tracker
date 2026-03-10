import {
  Field,
  FieldDescription,
  FieldError,
  FieldLabel,
} from 'app/components/ui/field'
import type {
  FieldPath,
  FieldValues,
  UseControllerReturn,
} from 'react-hook-form'

export type FormFieldProps<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
> = {
  label: string
  description?: string
  children: React.ReactNode
  controller: UseControllerReturn<TFieldValues, TName>
  htmlFor: string
}

export function FormField<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
>({
  label,
  description,
  children,
  controller,
  htmlFor,
}: FormFieldProps<TFieldValues, TName>) {
  const { fieldState } = controller
  return (
    <Field data-invalid={fieldState.invalid}>
      <FieldLabel htmlFor={htmlFor}>{label}</FieldLabel>
      {children}
      {description && <FieldDescription>{description}</FieldDescription>}
      {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
    </Field>
  )
}

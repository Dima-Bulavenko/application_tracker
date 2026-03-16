import { FieldPath, FieldValues, useController } from 'react-hook-form'
import type { BaseFormFiledProps } from 'shared/types/form'
import { DateInput } from 'shared/ui/DateInput'
import { FormField } from 'shared/ui/FormField'

export default function InterviewDateField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  label = 'Interview date',
  description,
  ...props
}: BaseFormFiledProps<V, N>) {
  const controller = useController({ ...props })
  const { field } = controller
  const id = `${field.name}_id`

  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <DateInput controller={controller} id={id} />
    </FormField>
  )
}

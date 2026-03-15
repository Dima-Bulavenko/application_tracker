import { FieldPath, FieldValues, useController } from 'react-hook-form'
import type { BaseFormFiledProps } from 'shared/types/form'
import { FormField } from 'shared/ui/FormField'
import { TextInput } from 'shared/ui/TextInput'

export default function ApplicationURLField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  label = 'Application URL',
  description,
  ...props
}: BaseFormFiledProps<V, N>) {
  const controller = useController({ ...props })
  const id = `${controller.field.name}_id`
  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <TextInput controller={controller} id={id} />
    </FormField>
  )
}

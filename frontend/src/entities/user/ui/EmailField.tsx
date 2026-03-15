import { FieldPath, FieldValues, useController } from 'react-hook-form'
import type { BaseFormFiledProps } from 'shared/types/form'
import { FormField } from 'shared/ui/FormField'
import { TextInput } from 'shared/ui/TextInput'

export default function EmailField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ label = 'Email', description, ...props }: BaseFormFiledProps<V, N>) {
  const controller = useController({ ...props })
  const id = `${controller.field.name}_id`
  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <TextInput type='email' controller={controller} id={id} />
    </FormField>
  )
}

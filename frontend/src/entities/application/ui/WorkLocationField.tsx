import { FieldPath, FieldValues, useController } from 'react-hook-form'
import { zWorkLocation } from 'shared/api/gen/zod.gen'
import type { BaseFormFiledProps } from 'shared/types/form'
import { FormField } from 'shared/ui/FormField'
import { SelectInput } from 'shared/ui/SelectInput'

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export function WorkLocationField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  label = 'Work Location',
  description,
  ...props
}: BaseFormFiledProps<V, N>) {
  const options = zWorkLocation.options
  const controller = useController({ ...props })
  const id = `${controller.field.name}_id`
  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <SelectInput
        {...props}
        options={options}
        controller={controller}
        id={id}
      />
    </FormField>
  )
}

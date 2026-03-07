import { useController } from 'react-hook-form'
import { zWorkType } from 'shared/api/gen/zod.gen'
import type { FieldComponent } from 'shared/types/form'
import { SelectField } from 'shared/ui/SelectField'

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const WorkTypeField: FieldComponent = ({
  label = 'Work Type',
  ...props
}) => {
  const options = zWorkType.options
  const controller = useController({ ...props })
  return (
    <SelectField
      {...props}
      label={label}
      options={options}
      controller={controller}
    />
  )
}

export default WorkTypeField

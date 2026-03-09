import { useController } from 'react-hook-form'
import { zAppStatus } from 'shared/api/gen/zod.gen'
import type { FieldComponent } from 'shared/types/form'
import { SelectField } from 'shared/ui/SelectField'

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const ApplicationStatusField: FieldComponent = ({
  label = 'Status',
  ...props
}) => {
  const options = zAppStatus.options
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

export default ApplicationStatusField

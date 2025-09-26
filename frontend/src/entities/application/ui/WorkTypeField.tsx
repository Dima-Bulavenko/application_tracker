import type { FieldComponent } from 'shared/types';
import { zWorkType } from 'shared/api/gen/zod.gen';
import { SelectField } from 'shared/ui/SelectField';
import { useController } from 'react-hook-form';

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const WorkTypeField: FieldComponent = ({
  label = 'Work Type',
  ...props
}) => {
  const options = zWorkType.options;
  const controller = useController({ ...props });
  return (
    <SelectField
      {...props}
      label={label}
      options={options}
      controller={controller}
    />
  );
};

export default WorkTypeField;

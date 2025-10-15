import type { FieldComponent } from 'shared/types/form';
import { zWorkLocation } from 'shared/api/gen/zod.gen';
import { SelectField } from 'shared/ui/SelectField';
import { useController } from 'react-hook-form';

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const WorkLocationField: FieldComponent = ({
  label = 'Work Location',
  ...props
}) => {
  const options = zWorkLocation.options;
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

export default WorkLocationField;

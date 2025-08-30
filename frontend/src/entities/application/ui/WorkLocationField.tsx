import { FieldComponent } from 'shared/types';
import { zWorkLocation } from 'shared/api/gen/zod.gen';
import { EnumSelectField } from 'shared/ui/EnumSelectField';

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const WorkLocationField: FieldComponent = ({
  label = 'Work Location',
  ...props
}) => {
  const options = zWorkLocation.options;
  return <EnumSelectField {...props} label={label} options={options} />;
};

export default WorkLocationField;

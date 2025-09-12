import { FieldComponent } from 'shared/types';
import { zAppStatus } from 'shared/api/gen/zod.gen';
import { EnumSelectField } from 'shared/ui/EnumSelectField';

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const ApplicationStatusField: FieldComponent = ({
  label = 'Status',
  ...props
}) => {
  const options = zAppStatus.options;
  return <EnumSelectField {...props} label={label} options={options} />;
};

export default ApplicationStatusField;

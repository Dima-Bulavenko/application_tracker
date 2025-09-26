import { useController } from 'react-hook-form';
import type { FieldComponent } from 'shared/types';
import { TextInput } from 'shared/ui';

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
const ApplicationURLField: FieldComponent = ({
  label = 'Application URL',
  ...props
}) => {
  const controller = useController(props);
  return <TextInput label={label} controller={controller} />;
};

export default ApplicationURLField;

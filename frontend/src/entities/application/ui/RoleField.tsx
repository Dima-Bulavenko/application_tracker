import { useController } from 'react-hook-form';
import { FieldComponent } from 'shared/types';
import { TextInput } from 'shared/ui';

const RoleField: FieldComponent = ({ label = 'Role', ...props }) => {
  const controller = useController(props);
  console.log(controller.formState.isSubmitting);
  return <TextInput label={label} {...controller} />;
};

export default RoleField;

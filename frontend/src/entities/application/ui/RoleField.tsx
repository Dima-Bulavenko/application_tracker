import { useController } from 'react-hook-form';
import type { FieldComponent } from 'shared/types';
import { TextInput } from 'shared/ui';

const RoleField: FieldComponent = ({ label = 'Role', ...props }) => {
  const controller = useController(props);
  return <TextInput label={label} controller={controller} />;
};

export default RoleField;

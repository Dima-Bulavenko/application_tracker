import { TextInput } from 'shared/ui/TextInput';
import type { FieldComponent } from 'shared/types/form';
import { useController } from 'react-hook-form';

const EmailField: FieldComponent = ({ label = 'Email', ...props }) => {
  const controller = useController(props);
  return <TextInput label={label} type='email' controller={controller} />;
};

export default EmailField;

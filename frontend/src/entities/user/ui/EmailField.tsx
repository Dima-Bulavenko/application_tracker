import { TextInput } from 'shared/ui';
import { type FieldComponent } from 'shared/types';
import { useController } from 'react-hook-form';

const EmailField: FieldComponent = ({ label = 'Email', ...props }) => {
  const controller = useController(props);
  return <TextInput label={label} type='email' {...controller} />;
};

export default EmailField;

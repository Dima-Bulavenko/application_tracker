import { type ChangeEvent } from 'react';
import { useController } from 'react-hook-form';
import { type FieldComponent } from 'shared/types';
import { TextInput } from 'shared/ui';

const CompanyField: FieldComponent = ({ label = 'Company', ...props }) => {
  const { field, fieldState, formState } = useController(props);
  const onChange = (event: ChangeEvent<HTMLInputElement>) => {
    field.onChange({ name: event.target.value });
  };
  return (
    <TextInput
      label={label}
      field={field}
      fieldState={fieldState}
      formState={formState}
      onChange={onChange}
    />
  );
};

export default CompanyField;

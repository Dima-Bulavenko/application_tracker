import { TextField } from '@mui/material';
import { useController } from 'react-hook-form';
import { FieldComponent } from 'shared/types';

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export const NoteField: FieldComponent = ({ label = 'Note', ...props }) => {
  const { field } = useController(props);
  return <TextField rows={3} multiline label={label} {...field} />;
};

export default NoteField;

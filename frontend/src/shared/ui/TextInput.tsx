import { TextField, TextFieldProps } from '@mui/material';
import {
  useController,
  FieldValues,
  FieldPath,
  UseControllerProps,
} from 'react-hook-form';
import { buildBaseInputProps } from 'shared/lib';

export function TextInput<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>(props: TextFieldProps & UseControllerProps<TFieldValues, TName>) {
  const { field, fieldState } = useController(props);
  const baseProps = buildBaseInputProps<TFieldValues, TName>(field, fieldState);
  return <TextField {...field} {...baseProps} {...props} />;
}

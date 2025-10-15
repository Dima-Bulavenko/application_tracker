import {
  FieldValues,
  FieldPath,
  ControllerRenderProps,
  ControllerFieldState,
} from 'react-hook-form';
import type { TextFieldProps } from '@mui/material/TextField';

export function buildBaseInputProps<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>(
  field: ControllerRenderProps<TFieldValues, TName>,
  fieldState: ControllerFieldState
): Pick<
  TextFieldProps,
  'id' | 'variant' | 'label' | 'value' | 'error' | 'helperText'
> {
  return {
    id: `${field.name}_id`,
    variant: 'outlined',
    label: field.name.charAt(0).toUpperCase() + field.name.slice(1),
    value: field.value || '',
    helperText: fieldState.error ? fieldState.error?.message : '',
    error: Boolean(fieldState.error),
  };
}

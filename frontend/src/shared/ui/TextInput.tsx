import TextField from '@mui/material/TextField';
import type { FieldValues, FieldPath } from 'react-hook-form';
import { TextInputProps } from 'shared/types/form';

export function TextInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ label, controller, children, helperText, ...props }: TextInputProps<V, N>) {
  const { field, fieldState, formState } = controller;
  return (
    <TextField
      variant='outlined'
      label={label}
      helperText={
        fieldState?.error?.message
          ? fieldState.error?.message
          : helperText
            ? helperText
            : ''
      }
      error={!!fieldState?.error}
      id={`${field.name}_id`}
      disabled={formState.isSubmitting || formState.isLoading || field.disabled}
      onBlur={field.onBlur}
      onChange={(e) => {
        const val = e.target.value;
        field.onChange(val.trim() === '' ? null : val);
      }}
      name={field.name}
      inputRef={field.ref}
      value={field.value ?? ''}
      {...props}>
      {children}
    </TextField>
  );
}

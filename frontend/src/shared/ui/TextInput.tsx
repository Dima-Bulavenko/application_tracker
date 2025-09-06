import { TextField, TextFieldProps } from '@mui/material';
import { FieldPath, FieldValues, UseControllerReturn } from 'react-hook-form';

type TextInputProps<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
> = Omit<TextFieldProps<'outlined'>, 'variant'> &
  UseControllerReturn<TFieldValues, TName>;

export function TextInput<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({
  label,
  field,
  fieldState,
  formState,
  ...props
}: TextInputProps<TFieldValues, TName>) {
  return (
    <TextField
      variant='outlined'
      label={label}
      helperText={
        fieldState?.error?.message
          ? fieldState.error?.message
          : props.helperText
            ? props.helperText
            : ''
      }
      error={!!fieldState?.error}
      id={`${field.name}_id`}
      disabled={formState.isSubmitting || formState.isLoading || field.disabled}
      onBlur={field.onBlur}
      onChange={field.onChange}
      name={field.name}
      ref={field.ref}
      value={field.value || ''}
      {...props}
    />
  );
}

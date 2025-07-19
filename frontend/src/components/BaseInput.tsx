import { TextField } from '@mui/material';
import { BaseInputProps } from '../types';
import React from 'react';
import { useController, FieldValues, FieldPath } from 'react-hook-form';

export default function BaseInput<
  T extends FieldValues,
  V extends FieldPath<T>,
>({ children = <TextField />, ...props }: BaseInputProps<T, V>) {
  const { field, fieldState } = useController(props);
  return React.cloneElement(children, {
    rules: { required: props?.required ? true : false },
    label: field.name.charAt(0).toUpperCase() + field.name.slice(1),
    variant: 'outlined',
    id: `${field.name}_id`,
    ...props,
    ...field,
    value: field.value || '',
    helperText: fieldState.error ? fieldState.error?.message : '',
    error: Boolean(fieldState.error),
  });
}

import { TextField } from '@mui/material';
import {
  FieldPath,
  FieldValues,
  UseControllerProps,
  useController,
} from 'react-hook-form';

type Props<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
> = UseControllerProps<TFieldValues, TName> & {
  control: NonNullable<UseControllerProps<TFieldValues, TName>['control']>;
  label?: string;
};

/**
 * Application status select field integrated with react-hook-form.
 * Values are sourced from generated zod enum to stay in sync with API.
 */
export function ApplicationURLField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({ label = 'Application URL', ...props }: Props<TFieldValues, TName>) {
  const { field, fieldState } = useController(props);
  return (
    <TextField
      label={label}
      {...field}
      error={!!fieldState.error}
      helperText={fieldState.error?.message ?? ''}
    />
  );
}

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

export default function CompanyField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({ label = 'Company', ...props }: Props<TFieldValues, TName>) {
  const { field, fieldState } = useController(props);
  return (
    <TextField
      label={label}
      {...field}
      error={!!fieldState.error}
      helperText={fieldState.error?.message ?? ''}
      required
    />
  );
}

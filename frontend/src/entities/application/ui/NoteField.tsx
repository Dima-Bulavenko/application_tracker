import { TextField } from '@mui/material';
import {
  FieldPath,
  FieldValues,
  useController,
  UseControllerProps,
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
export function NoteField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({ label = 'Note', ...props }: Props<TFieldValues, TName>) {
  const { field } = useController(props);
  return <TextField rows={3} multiline label={label} {...field} />;
}

export default NoteField;

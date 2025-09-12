import {
  FormControl,
  FormControlProps,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import {
  FieldPath,
  FieldValues,
  UseControllerProps,
  useController,
} from 'react-hook-form';

type BaseProps<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
> = UseControllerProps<TFieldValues, TName> &
  Pick<FormControlProps, 'fullWidth' | 'disabled' | 'size' | 'variant'> & {
    label?: string;
    options: readonly string[];
    humanize?: (v: string) => string;
  };

export function EnumSelectField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({
  label,
  options,
  humanize,
  fullWidth = true,
  disabled,
  size,
  variant,
  ...controllerProps
}: BaseProps<TFieldValues, TName>) {
  const { field, fieldState } = useController(controllerProps);

  const id = `${field.name}_id`;
  const labelId = `${id}_label`;

  const toLabel =
    humanize ??
    ((v: string) => v.charAt(0).toUpperCase() + v.slice(1).replace('_', ' '));

  return (
    <FormControl
      fullWidth={fullWidth}
      disabled={disabled}
      error={!!fieldState.error}
      size={size}
      variant={variant}>
      {label && <InputLabel id={labelId}>{label}</InputLabel>}
      <Select
        {...field}
        labelId={label ? labelId : undefined}
        id={id}
        label={label}>
        {options.map((opt) => (
          <MenuItem key={opt} value={opt}>
            {toLabel(opt)}
          </MenuItem>
        ))}
      </Select>
      {fieldState.error && (
        <FormHelperText>{fieldState.error.message}</FormHelperText>
      )}
    </FormControl>
  );
}

export default EnumSelectField;

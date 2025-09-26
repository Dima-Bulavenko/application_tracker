import { Checkbox, ListItemText, MenuItem } from '@mui/material';

import { TextInput } from './TextInput';
import type { SelectInputProps, SelectMultipleProps } from 'shared/types';
import { FieldPath, FieldValues } from 'react-hook-form';

const defaultHumanize = (v: string) =>
  v.charAt(0).toUpperCase() + v.slice(1).replace('_', ' ');

const defaultRenderValue = (s: unknown) =>
  Array.isArray(s) ? s.join(', ') : '';

export function SelectField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  humanize = defaultHumanize,
  options,
  children,
  controller,
  ...props
}: SelectInputProps<V, N>) {
  const { field } = controller;
  return (
    <TextInput
      select
      controller={controller}
      onChange={(e) => {
        field.onChange(e);
      }}
      {...props}>
      {children
        ? children
        : options.map((opt) => (
            <MenuItem key={opt} value={opt}>
              {humanize(opt)}
            </MenuItem>
          ))}
    </TextInput>
  );
}

export function MultipleSelectField({
  options,
  controller,
  humanize = defaultHumanize,
  renderValue = defaultRenderValue,
  ...props
}: SelectMultipleProps) {
  const { field } = controller;
  return (
    <SelectField
      options={options}
      slotProps={{
        select: {
          multiple: true,
          renderValue,
        },
      }}
      controller={controller}
      {...props}>
      {options.map((opt) => (
        <MenuItem key={opt} value={opt}>
          <Checkbox
            checked={
              Array.isArray(field.value) ? field.value.includes(opt) : false
            }
          />
          <ListItemText primary={humanize(opt)} />
        </MenuItem>
      ))}
    </SelectField>
  );
}

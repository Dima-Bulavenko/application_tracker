import { Checkbox, ListItemText, MenuItem } from '@mui/material';
import { TextInput } from './TextInput';
import { type UseControllerReturn } from 'react-hook-form';
import { ReactNode } from 'react';

type SelectMultipleProps = {
  label: string;
  controller: UseControllerReturn;
  readonly options: string[];
  humanize?: (v: string) => string;
  renderValue?: (v: unknown) => ReactNode;
};

const humanizeOptions = (v: string) =>
  v.charAt(0).toUpperCase() + v.slice(1).replace('_', ' ');

const defaultRenderValue = (s: unknown) =>
  Array.isArray(s) ? s.join(', ') : '';

export function MultipleSelectField({
  options,
  controller,
  humanize = humanizeOptions,
  renderValue,
  ...props
}: SelectMultipleProps) {
  const { field } = controller;
  return (
    <TextInput
      select
      slotProps={{
        select: {
          multiple: true,
          renderValue: renderValue || defaultRenderValue,
        },
      }}
      onChange={(e) => {
        field.onChange(e);
      }}
      {...controller}
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
    </TextInput>
  );
}

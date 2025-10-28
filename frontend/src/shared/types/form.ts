import type { TextFieldProps } from '@mui/material/TextField';
import type { ReactNode } from 'react';
import type {
  UseControllerProps,
  Control,
  UseControllerReturn,
  FieldValues,
  FieldPath,
} from 'react-hook-form';

export type BaseInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<UseControllerProps<V, N>, 'control'> & {
  control: Control<V, N>;
  label?: string;
};

export type FieldComponent = <
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>(
  props: BaseInputProps<V, N>
) => JSX.Element;

export type TextInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<TextFieldProps<'outlined'>, 'variant'> & {
  controller: UseControllerReturn<V, N>;
};

export type SelectInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = TextInputProps<V, N> & {
  options: readonly string[];
  humanize?: (v: string) => string;
};

export type SelectMultipleProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = SelectInputProps<V, N> & {
  renderValue?: (v: unknown) => ReactNode;
};

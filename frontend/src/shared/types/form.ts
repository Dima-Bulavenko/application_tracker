import type {
  FieldPath,
  FieldValues,
  UseControllerProps,
  Control,
} from 'react-hook-form';

export type RequiredControl<TFV extends FieldValues> = Control<TFV>;

export type FieldProps<
  TFV extends FieldValues,
  TName extends FieldPath<TFV>,
> = Omit<UseControllerProps<TFV, TName>, 'control'> & {
  control: RequiredControl<TFV>;
  label?: string;
};

export type FieldComponent = <
  TFV extends FieldValues,
  TName extends FieldPath<TFV>,
>(
  props: FieldProps<TFV, TName>
) => JSX.Element;

import { FieldPath, FieldValues, UseControllerProps } from 'react-hook-form';
import { zWorkLocation } from 'shared/api/gen/zod.gen';
import { EnumSelectField } from 'shared/ui/EnumSelectField';

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
export function WorkLocationField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({ label = 'Work Location', ...props }: Props<TFieldValues, TName>) {
  const options = zWorkLocation.options;
  return <EnumSelectField {...props} label={label} options={options} />;
}

export default WorkLocationField;

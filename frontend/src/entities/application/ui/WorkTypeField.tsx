import { FieldPath, FieldValues, UseControllerProps } from 'react-hook-form';
import { zWorkType } from 'shared/api/gen/zod.gen';
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
export function WorkTypeField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({ label = 'Work Type', ...props }: Props<TFieldValues, TName>) {
  const options = zWorkType.options;
  return <EnumSelectField {...props} label={label} options={options} />;
}

export default WorkTypeField;

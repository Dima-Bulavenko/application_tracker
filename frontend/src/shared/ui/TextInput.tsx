import { InputGroup, InputGroupInput } from 'app/components/ui/input-group'
import type {
  FieldPath,
  FieldValues,
  UseControllerReturn,
} from 'react-hook-form'

type TextInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = { controller: UseControllerReturn<V, N>; id: string } & Omit<
  React.ComponentProps<'input'>,
  'name' | 'value' | 'onChange' | 'id'
>

export function TextInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ controller, children, ...props }: TextInputProps<V, N>) {
  const { field, fieldState, formState } = controller

  return (
    <InputGroup>
      <InputGroupInput
        name={field.name}
        value={field.value}
        onChange={field.onChange}
        aria-invalid={fieldState.invalid}
        disabled={formState.isSubmitting}
        {...props}
      />
      {children}
    </InputGroup>
  )
}

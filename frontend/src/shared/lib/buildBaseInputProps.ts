import type {
  ControllerFieldState,
  ControllerRenderProps,
  FieldPath,
  FieldValues,
} from 'react-hook-form'

export function buildBaseInputProps<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>(
  field: ControllerRenderProps<TFieldValues, TName>,
  fieldState: ControllerFieldState
) {
  return {
    id: `${field.name}_id`,
    label: field.name.charAt(0).toUpperCase() + field.name.slice(1),
    value: field.value || '',
    helperText: fieldState.error ? fieldState.error?.message : '',
    error: Boolean(fieldState.error),
  }
}

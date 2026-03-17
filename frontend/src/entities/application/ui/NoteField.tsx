import { FieldPath, FieldValues, useController } from 'react-hook-form'
import type { BaseFormFiledProps } from 'shared/types/form'
import { TextareaInput } from 'shared/ui/TextareaInput'

export function NoteField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
  TTransformedValues = V,
>({ label = 'Note', ...props }: BaseFormFiledProps<V, N, TTransformedValues>) {
  const controller = useController({ ...props })
  return <TextareaInput rows={3} label={label} controller={controller} />
}

export default NoteField

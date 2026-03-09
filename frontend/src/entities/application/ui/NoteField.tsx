import { useController } from 'react-hook-form'
import type { FieldComponent } from 'shared/types/form'
import { TextareaInput } from 'shared/ui/TextareaInput'

export const NoteField: FieldComponent = ({ label = 'Note', ...props }) => {
  const controller = useController(props)
  return <TextareaInput rows={3} label={label} controller={controller} />
}

export default NoteField

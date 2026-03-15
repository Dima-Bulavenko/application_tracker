import { zodResolver } from '@hookform/resolvers/zod'
import { getRouteApi } from '@tanstack/react-router'
import { type SubmitHandler, useController, useForm } from 'react-hook-form'
import { updateUser } from 'shared/api/gen'
import { zUserUpdate } from 'shared/api/gen/zod.gen'
import { getDirtyValues } from 'shared/api/get_dirty_values'
import { Form } from 'shared/ui/Form'
import { FormError } from 'shared/ui/FormError'
import SubmitButton from 'shared/ui/SubmitButton'
import { TextInput } from 'shared/ui/TextInput'
import { z } from 'zod'

type FormType = z.infer<typeof zUserUpdate>

const FirstNameField: FieldComponent = ({ label = 'First Name', ...props }) => {
  const controller = useController(props)
  return <TextInput label={label} controller={controller} />
}

const SecondNameField: FieldComponent = ({
  label = 'Second Name',
  ...props
}) => {
  const controller = useController(props)
  return <TextInput label={label} controller={controller} />
}

const routeApi = getRouteApi('/_authenticated')

type UpdateFormProps = {
  onSuccess?: () => void
}

export function UpdateForm({ onSuccess }: UpdateFormProps = {}) {
  const {
    auth: { user, setUser },
  } = routeApi.useRouteContext()
  const {
    control,
    handleSubmit,
    formState: { errors, isDirty, dirtyFields, isSubmitting },
  } = useForm<FormType>({
    resolver: zodResolver(zUserUpdate),
    defaultValues: {
      first_name: user.first_name,
      second_name: user.second_name,
    },
  })
  const onSubmit: SubmitHandler<FormType> = async (data, event) => {
    event?.preventDefault()
    const dirtyData = getDirtyValues(dirtyFields, data)
    await updateUser<true>({ body: dirtyData }).then((res) => {
      setUser(res.data)
      onSuccess?.()
    })
  }
  return (
    <Form onSubmit={handleSubmit(onSubmit)} className='max-w-full p-0'>
      <div className='space-y-3'>
        <FirstNameField name='first_name' control={control} />
        <SecondNameField name='second_name' control={control} />
        <FormError message={errors.root?.message} />
        <div className='flex justify-end pt-1'>
          <SubmitButton
            disabled={!isDirty || isSubmitting}
            isSubmitting={isSubmitting}
          >
            Save Changes
          </SubmitButton>
        </div>
      </div>
    </Form>
  )
}

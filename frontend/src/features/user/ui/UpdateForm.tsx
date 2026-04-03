import { zodResolver } from '@hookform/resolvers/zod'
import { getRouteApi } from '@tanstack/react-router'
import {
  FieldPath,
  FieldValues,
  type SubmitHandler,
  useController,
  useForm,
} from 'react-hook-form'
import { updateUser } from 'shared/api/gen'
import { getDirtyValues } from 'shared/api/get_dirty_values'
import type { BaseFormFiledProps } from 'shared/types/form'
import { Form } from 'shared/ui/Form'
import { FormError } from 'shared/ui/FormError'
import { FormField } from 'shared/ui/FormField'
import SubmitButton from 'shared/ui/SubmitButton'
import { TextInput } from 'shared/ui/TextInput'
import { toast } from 'sonner'
import { z } from 'zod'

const nullableTextSchema = z.preprocess((value: string) => {
  if (typeof value !== 'string') {
    return value
  }

  const trimmedValue = value.trim()
  return trimmedValue === '' ? null : trimmedValue
}, z.string().max(40).nullable())

const updateUserFormSchema = z.object({
  first_name: nullableTextSchema,
  second_name: nullableTextSchema,
})

type InputT = z.input<typeof updateUserFormSchema>
type OutputT = z.output<typeof updateUserFormSchema>

function FirstNameField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
  TTransformedValues = V,
>({
  label = 'First Name',
  description,
  ...props
}: BaseFormFiledProps<V, N, TTransformedValues>) {
  const controller = useController({ ...props })
  const id = `${controller.field.name}_id`
  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <TextInput controller={controller} id={id} />
    </FormField>
  )
}

function SecondNameField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
  TTransformedValues = V,
>({
  label = 'Second Name',
  description,
  ...props
}: BaseFormFiledProps<V, N, TTransformedValues>) {
  const controller = useController({ ...props })
  const id = `${controller.field.name}_id`
  return (
    <FormField
      label={label}
      controller={controller}
      htmlFor={id}
      description={description}
    >
      <TextInput controller={controller} id={id} />
    </FormField>
  )
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
  } = useForm<InputT, unknown, OutputT>({
    resolver: zodResolver(updateUserFormSchema),
    defaultValues: {
      first_name: user.first_name ?? '',
      second_name: user.second_name ?? '',
    },
  })
  const onSubmit: SubmitHandler<OutputT> = async (data, event) => {
    event?.preventDefault()
    const dirtyData = getDirtyValues(dirtyFields, data)
    await updateUser<true>({ body: dirtyData }).then((res) => {
      setUser(res.data)
      toast.success('Profile updated successfully')
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

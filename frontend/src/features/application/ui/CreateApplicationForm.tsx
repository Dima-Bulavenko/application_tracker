import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { applicationCreateOptions } from 'entities/application/api/queryOptions'
import { ApplicationStatusField } from 'entities/application/ui/ApplicationStatusField'
import ApplicationURLField from 'entities/application/ui/ApplicationURLField'
import CompanyField from 'entities/application/ui/CompanyField'
import InterviewDateField from 'entities/application/ui/InterviewDateField'
import { NoteField } from 'entities/application/ui/NoteField'
import RoleField from 'entities/application/ui/RoleField'
import { WorkLocationField } from 'entities/application/ui/WorkLocationField'
import { WorkTypeField } from 'entities/application/ui/WorkTypeField'
import { type SubmitHandler, useForm } from 'react-hook-form'
import { zAppStatus, zWorkLocation, zWorkType } from 'shared/api/gen/zod.gen'
import { Form } from 'shared/ui/Form'
import { FormError } from 'shared/ui/FormError'
import SubmitButton from 'shared/ui/SubmitButton'
import { z } from 'zod'

const nullableTextSchema = z.preprocess((value: string) => {
  if (typeof value !== 'string') {
    return value
  }

  const trimmedValue = value.trim()
  return trimmedValue === '' ? null : trimmedValue
}, z.string().nullable())

const nullableIsoDatetimeSchema = z.preprocess(
  (value: string) => (value === '' ? null : value),
  z.iso.datetime({ offset: true }).nullable()
)

const createApplicationFormSchema = z.object({
  role: z.string().trim().min(1, 'Role is required').max(40),
  company: z.object({
    name: z.string().trim().min(1, 'Company is required').max(40),
  }),
  status: zAppStatus,
  work_type: zWorkType,
  work_location: zWorkLocation,
  note: nullableTextSchema,
  application_url: nullableTextSchema,
  interview_date: nullableIsoDatetimeSchema,
})

type InputT = z.input<typeof createApplicationFormSchema>
type OutputT = z.output<typeof createApplicationFormSchema>

interface CreateApplicationFormProps {
  onSuccess?: () => void
}

export function CreateApplicationForm({
  onSuccess,
}: CreateApplicationFormProps) {
  const defaultValues: InputT = {
    application_url: '',
    company: { name: '' },
    note: '',
    role: '',
    status: 'applied',
    work_type: 'full_time',
    work_location: 'on_site',
    interview_date: '',
  }
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<InputT, unknown, OutputT>({
    resolver: zodResolver(createApplicationFormSchema),
    defaultValues,
  })
  const { mutate: createApp, isPending } = useMutation(
    applicationCreateOptions()
  )
  const onSubmit: SubmitHandler<OutputT> = (data, event) => {
    event?.preventDefault()
    createApp(data, {
      onSuccess: () => {
        reset(defaultValues)
        onSuccess?.()
      },
    })
  }
  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <div className='space-y-5'>
        <RoleField name='role' control={control} />
        <CompanyField name='company.name' control={control} />
        <ApplicationStatusField name='status' control={control} />
        <WorkTypeField name='work_type' control={control} />
        <WorkLocationField name='work_location' control={control} />
        <NoteField name='note' control={control} />
        <InterviewDateField name='interview_date' control={control} />
        <ApplicationURLField name='application_url' control={control} />
      </div>
      <FormError message={errors.root?.message} />
      <SubmitButton isSubmitting={isPending}>Create Application</SubmitButton>
    </Form>
  )
}

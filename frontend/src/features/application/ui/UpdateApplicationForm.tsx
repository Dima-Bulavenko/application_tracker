import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { Button } from 'app/components/ui/button'
import { applicationUpdateOptions } from 'entities/application/api/queryOptions'
import { ApplicationStatusField } from 'entities/application/ui/ApplicationStatusField'
import ApplicationURLField from 'entities/application/ui/ApplicationURLField'
import CompanyField from 'entities/application/ui/CompanyField'
import InterviewDateField from 'entities/application/ui/InterviewDateField'
import { NoteField } from 'entities/application/ui/NoteField'
import RoleField from 'entities/application/ui/RoleField'
import { WorkLocationField } from 'entities/application/ui/WorkLocationField'
import { WorkTypeField } from 'entities/application/ui/WorkTypeField'
import { type SubmitHandler, useForm } from 'react-hook-form'
import type {
  ApplicationRead,
  ApplicationUpdate,
} from 'shared/api/gen/types.gen'
import { zApplicationUpdate } from 'shared/api/gen/zod.gen'
import { getDirtyValues } from 'shared/api/get_dirty_values'
import { Form } from 'shared/ui/Form'
import { FormError } from 'shared/ui/FormError'
import SubmitButton from 'shared/ui/SubmitButton'

export function UpdateApplicationForm(defaultValues: ApplicationRead) {
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, dirtyFields, isDirty },
  } = useForm<ApplicationUpdate>({
    resolver: zodResolver(zApplicationUpdate),
    defaultValues,
  })
  const { mutate: updateApp, isPending } = useMutation(
    applicationUpdateOptions(defaultValues.id)
  )
  const onSubmit: SubmitHandler<ApplicationUpdate> = async (data, event) => {
    event?.preventDefault()
    const newData = getDirtyValues(dirtyFields, data)
    if (newData) {
      updateApp(newData)
    }
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
      <SubmitButton isSubmitting={isPending} disabled={!isDirty || isPending}>
        Update Application
      </SubmitButton>
      <Button
        type='button'
        variant='outline'
        disabled={!isDirty}
        onClick={() => reset()}
        className='mt-3'
      >
        Reset Form
      </Button>
    </Form>
  )
}

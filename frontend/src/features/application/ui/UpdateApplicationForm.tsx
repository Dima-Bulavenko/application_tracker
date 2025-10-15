import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { useUpdateApplication } from 'entities/application/api/useApplications';
import { ApplicationStatusField } from 'entities/application/ui/ApplicationStatusField';
import { WorkTypeField } from 'entities/application/ui/WorkTypeField';
import { WorkLocationField } from 'entities/application/ui/WorkLocationField';
import { NoteField } from 'entities/application/ui/NoteField';
import InterviewDateField from 'entities/application/ui/InterviewDateField';
import RoleField from 'entities/application/ui/RoleField';
import CompanyField from 'entities/application/ui/CompanyField';
import ApplicationURLField from 'entities/application/ui/ApplicationURLField';
import { SubmitHandler, useForm } from 'react-hook-form';
import type {
  ApplicationUpdate,
  ApplicationRead,
} from 'shared/api/gen/types.gen';
import { getDirtyValues } from 'shared/api/get_dirty_values';
import { zApplicationUpdate } from 'shared/api/gen/zod.gen';
import { customZodResolver } from 'shared/lib/customZodResolver';
import { Form } from 'shared/ui/Form';
import { FormError } from 'shared/ui/FormError';

export function UpdateApplicationForm(defaultValues: ApplicationRead) {
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, dirtyFields, isDirty },
  } = useForm<ApplicationUpdate>({
    resolver: customZodResolver(zApplicationUpdate),
    defaultValues,
  });
  const { mutate: updateApp } = useUpdateApplication(defaultValues.id);
  const onSubmit: SubmitHandler<ApplicationUpdate> = async (data, event) => {
    event?.preventDefault();
    const newData = getDirtyValues(dirtyFields, data);
    if (newData) {
      updateApp(newData);
    }
  };
  return (
    <>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={5}>
          <RoleField name='role' control={control} />
          <CompanyField name='company.name' control={control} />
          <ApplicationStatusField name='status' control={control} />
          <WorkTypeField name='work_type' control={control} />
          <WorkLocationField name='work_location' control={control} />
          <NoteField name='note' control={control} />
          <InterviewDateField name='interview_date' control={control} />
          <ApplicationURLField name='application_url' control={control} />
        </Stack>
        <FormError message={errors.root?.message} />
        <Button
          sx={{ mt: 5 }}
          type='submit'
          color='primary'
          disabled={!isDirty}
          variant='contained'>
          UpdateApplicationForm Application
        </Button>
        <Button
          sx={{ mt: 3 }}
          type='button'
          color='primary'
          disabled={!isDirty}
          onClick={() => reset()}
          variant='contained'>
          Reset Form
        </Button>
      </Form>
    </>
  );
}

import { Button, Stack } from '@mui/material';
import { useUpdateApplication } from 'entities/application/api';
import {
  ApplicationStatusField,
  WorkTypeField,
  WorkLocationField,
  NoteField,
  InterviewDateField,
  RoleField,
  CompanyField,
  ApplicationURLField,
} from 'entities/application/ui';
import { SubmitHandler, useForm } from 'react-hook-form';
import {
  type ApplicationUpdate,
  type ApplicationRead,
  getDirtyValues,
  zApplicationUpdate,
} from 'shared/api';
import { customZodResolver } from 'shared/lib';
import { Form, FormError } from 'shared/ui';

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

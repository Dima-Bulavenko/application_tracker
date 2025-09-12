import { Button, Stack } from '@mui/material';
import { useCreateApplication } from 'entities/application/api';
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
import { zApplicationCreate, type ApplicationCreate } from 'shared/api';
import { customZodResolver } from 'shared/lib';
import { Form, FormError } from 'shared/ui';

export default function CreateApplicationForm() {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<ApplicationCreate>({
    resolver: customZodResolver(zApplicationCreate),
    defaultValues: {
      status: 'applied',
      work_type: 'full_time',
      work_location: 'on_site',
    },
  });
  const { mutate: createApp } = useCreateApplication();
  const onSubmit: SubmitHandler<ApplicationCreate> = (data, event) => {
    event?.preventDefault();
    createApp(data);
  };
  return (
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
      <Button sx={{ mt: 5 }} type='submit' color='primary' variant='contained'>
        Create Application
      </Button>
    </Form>
  );
}

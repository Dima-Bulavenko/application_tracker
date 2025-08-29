import { Button, Stack } from '@mui/material';
import {
  ApplicationStatusField,
  WorkTypeField,
  WorkLocationField,
  NoteField,
  InterviewDateField,
} from 'entities/application/ui';
import { ApplicationURLField } from 'entities/application/ui/ApplicationURLField';
import { SubmitHandler, useForm } from 'react-hook-form';
import {
  createApplication,
  zApplicationCreate,
  type ApplicationCreate,
} from 'shared/api';
import { customZodResolver } from 'shared/lib';
import { Form, FormError, TextInput } from 'shared/ui';

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
  const onSubmit: SubmitHandler<ApplicationCreate> = (data, event) => {
    event?.preventDefault();
    createApplication({ body: data }).then((response) => {
      console.log(response);
    });
  };
  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={5}>
        <TextInput
          name='role'
          required
          control={control}
          rules={{ required: true }}
        />
        <TextInput
          name='company'
          required
          control={control}
          rules={{ required: true }}
        />
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

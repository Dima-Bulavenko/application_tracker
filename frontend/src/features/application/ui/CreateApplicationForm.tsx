import Stack from '@mui/material/Stack';
import { applicationCreateOptions } from 'entities/application/api/queryOptions';
import { ApplicationStatusField } from 'entities/application/ui/ApplicationStatusField';
import { WorkTypeField } from 'entities/application/ui/WorkTypeField';
import { WorkLocationField } from 'entities/application/ui/WorkLocationField';
import { NoteField } from 'entities/application/ui/NoteField';
import InterviewDateField from 'entities/application/ui/InterviewDateField';
import RoleField from 'entities/application/ui/RoleField';
import CompanyField from 'entities/application/ui/CompanyField';
import ApplicationURLField from 'entities/application/ui/ApplicationURLField';
import { SubmitHandler, useForm } from 'react-hook-form';
import { type ApplicationCreate } from 'shared/api/gen/types.gen';
import { zApplicationCreate } from 'shared/api/gen/zod.gen';
import { customZodResolver } from 'shared/lib/customZodResolver';
import { Form } from 'shared/ui/Form';
import { FormError } from 'shared/ui/FormError';
import { useMutation } from '@tanstack/react-query';
import SubmitButton from 'shared/ui/SubmitButton';

export function CreateApplicationForm() {
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
      interview_date: null,
    },
  });
  const { mutate: createApp, isPending } = useMutation(
    applicationCreateOptions()
  );
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
      <SubmitButton isSubmitting={isPending}>Create Application</SubmitButton>
    </Form>
  );
}

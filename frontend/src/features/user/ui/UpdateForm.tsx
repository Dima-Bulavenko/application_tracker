import { useForm, useController, SubmitHandler } from 'react-hook-form';
import { zUserUpdate } from 'shared/api/gen/zod.gen';
import { customZodResolver } from 'shared/lib/customZodResolver';
import { Form } from 'shared/ui/Form';
import type { FieldComponent } from 'shared/types/form';
import { z } from 'zod';
import { TextInput } from 'shared/ui/TextInput';
import { FormError } from 'shared/ui/FormError';
import Stack from '@mui/material/Stack';
import { DevTool } from '@hookform/devtools';
import { updateUser } from 'shared/api/gen';
import { getDirtyValues } from 'shared/api/get_dirty_values';
import { getRouteApi } from '@tanstack/react-router';
import SubmitButton from 'shared/ui/SubmitButton';

type FormType = z.infer<typeof zUserUpdate>;

const FirstNameField: FieldComponent = ({ label = 'First Name', ...props }) => {
  const controller = useController(props);
  return <TextInput label={label} controller={controller} />;
};

const SecondNameField: FieldComponent = ({
  label = 'Second Name',
  ...props
}) => {
  const controller = useController(props);
  return <TextInput label={label} controller={controller} />;
};

const routeApi = getRouteApi('/_authenticated');

export function UpdateForm() {
  const {
    auth: { user, setUser },
  } = routeApi.useRouteContext();
  const {
    control,
    handleSubmit,
    formState: { errors, isDirty, dirtyFields, isSubmitting },
  } = useForm<FormType>({
    resolver: customZodResolver(zUserUpdate),
    defaultValues: {
      first_name: user.first_name,
      second_name: user.second_name,
    },
  });
  const onSubmit: SubmitHandler<FormType> = async (data, event) => {
    event?.preventDefault();
    const dirtyData = getDirtyValues(dirtyFields, data);
    await updateUser<true>({ body: dirtyData }).then((res) =>
      setUser(res.data)
    );
  };
  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={5}>
        <FirstNameField name='first_name' control={control} />
        <SecondNameField name='second_name' control={control} />
        <FormError message={errors.root?.message} />
      </Stack>
      <SubmitButton
        disabled={!isDirty || isSubmitting}
        isSubmitting={isSubmitting}>
        Update
      </SubmitButton>
      <DevTool control={control} />
    </Form>
  );
}

import { useForm, useController, SubmitHandler } from 'react-hook-form';
import { zUserUpdate } from 'shared/api/gen/zod.gen';
import { customZodResolver } from 'shared/lib/customZodResolver';
import { Form } from 'shared/ui/Form';
import type { FieldComponent } from 'shared/types/form';
import { z } from 'zod';
import { TextInput } from 'shared/ui/TextInput';
import { FormError } from 'shared/ui/FormError';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { DevTool } from '@hookform/devtools';
import { updateUser } from 'shared/api/gen';
import { getDirtyValues } from 'shared/api/get_dirty_values';
import { getRouteApi } from '@tanstack/react-router';

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
    auth: { user },
  } = routeApi.useRouteContext();
  const {
    control,
    handleSubmit,
    formState: { errors, isDirty, dirtyFields },
  } = useForm<FormType>({
    resolver: customZodResolver(zUserUpdate),
    defaultValues: {
      first_name: user.first_name,
      second_name: user.second_name,
    },
  });
  const onSubmit: SubmitHandler<FormType> = (data, event) => {
    event?.preventDefault();
    const dirtyData = getDirtyValues(dirtyFields, data);
    updateUser<true>({ body: dirtyData }).then((res) => setUser(res.data));
  };
  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={5}>
        <FirstNameField name='first_name' control={control} />
        <SecondNameField name='second_name' control={control} />
        <FormError message={errors.root?.message} />
      </Stack>
      <Button
        disabled={!isDirty}
        sx={{ mt: 5 }}
        type='submit'
        color='primary'
        variant='contained'>
        Update
      </Button>
      <DevTool control={control} />
    </Form>
  );
}

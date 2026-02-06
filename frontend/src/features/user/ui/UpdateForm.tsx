import { useForm, useController, SubmitHandler } from 'react-hook-form';
import { zUserUpdate } from 'shared/api/gen/zod.gen';
import { Form } from 'shared/ui/Form';
import type { FieldComponent } from 'shared/types/form';
import { z } from 'zod';
import { TextInput } from 'shared/ui/TextInput';
import { FormError } from 'shared/ui/FormError';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import { updateUser } from 'shared/api/gen';
import { getDirtyValues } from 'shared/api/get_dirty_values';
import { getRouteApi } from '@tanstack/react-router';
import SubmitButton from 'shared/ui/SubmitButton';
import { zodResolver } from '@hookform/resolvers/zod';

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

type UpdateFormProps = {
  onSuccess?: () => void;
};

export function UpdateForm({ onSuccess }: UpdateFormProps = {}) {
  const {
    auth: { user, setUser },
  } = routeApi.useRouteContext();
  const {
    control,
    handleSubmit,
    formState: { errors, isDirty, dirtyFields, isSubmitting },
  } = useForm<FormType>({
    resolver: zodResolver(zUserUpdate),
    defaultValues: {
      first_name: user.first_name,
      second_name: user.second_name,
    },
  });
  const onSubmit: SubmitHandler<FormType> = async (data, event) => {
    event?.preventDefault();
    const dirtyData = getDirtyValues(dirtyFields, data);
    await updateUser<true>({ body: dirtyData }).then((res) => {
      setUser(res.data);
      onSuccess?.();
    });
  };
  return (
    <Form
      onSubmit={handleSubmit(onSubmit)}
      sx={{ p: 0, m: 0, maxWidth: '100%' }}>
      <Stack spacing={3}>
        <FirstNameField name='first_name' control={control} />
        <SecondNameField name='second_name' control={control} />
        <FormError message={errors.root?.message} />
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', pt: 1 }}>
          <SubmitButton
            disabled={!isDirty || isSubmitting}
            isSubmitting={isSubmitting}>
            Save Changes
          </SubmitButton>
        </Box>
      </Stack>
    </Form>
  );
}

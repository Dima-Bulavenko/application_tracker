import { Form } from 'shared/ui/Form';
import { FormError } from 'shared/ui/FormError';
import type { UserCreate } from 'shared/api/gen/types.gen';
import { createUser } from 'shared/api/gen/sdk.gen';
import { zUserCreate } from 'shared/api/gen/zod.gen';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { customZodResolver } from 'shared/lib/customZodResolver';
import { useNavigate } from '@tanstack/react-router';
import EmailField from 'entities/user/ui/EmailField';
import PasswordField from 'entities/user/ui/PasswordField';

export default function RegisterForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<UserCreate>({ resolver: customZodResolver(zUserCreate) });

  const navigate = useNavigate();

  const onSubmit: SubmitHandler<UserCreate> = async (data, event) => {
    event?.preventDefault();
    const res = await createUser({ body: data });
    if (res.status === 201) {
      navigate({ to: '/sing-in', replace: true });
      return;
    }
    setError('root', { message: 'Registration failed. Please try again.' });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={5}>
        <EmailField name='username' control={control} />
        <PasswordField name='password' control={control} />
      </Stack>
      <FormError message={errors.root?.message} />
      <Button sx={{ mt: 5 }} type='submit' color='primary' variant='contained'>
        Sign Up
      </Button>
    </Form>
  );
}

import { Form } from 'shared/ui/Form';
import { FormError } from 'shared/ui/FormError';
import type { UserLogin } from 'shared/api/gen/types.gen';
import { zUserLogin } from 'shared/api/gen/zod.gen';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { useForm, SubmitHandler } from 'react-hook-form';
import { customZodResolver } from 'shared/lib/customZodResolver';
import { getRouteApi } from '@tanstack/react-router';
import EmailField from 'entities/user/ui/EmailField';
import PasswordField from 'entities/user/ui/PasswordField';

const routeApi = getRouteApi('/sign-in');

export default function SignInForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<UserLogin>({
    resolver: customZodResolver(zUserLogin),
  });
  const {
    auth: { login },
  } = routeApi.useRouteContext();
  const onSubmit: SubmitHandler<UserLogin> = async (data, event) => {
    event?.preventDefault();
    login(data).catch((err) => {
      if (err.status === 401) {
        setError('root', { message: 'Invalid email or password' });
      }
    });
  };
  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={5}>
        <EmailField name='username' control={control} />
        <PasswordField name='password' control={control} />
      </Stack>
      <FormError message={errors.root?.message} />
      <Button sx={{ mt: 5 }} type='submit' color='primary' variant='contained'>
        Sign In
      </Button>
    </Form>
  );
}

import { Form } from 'shared/ui/Form';
import { FormError } from 'shared/ui/FormError';
import type { UserLogin } from 'shared/api/gen/types.gen';
import { zUserLogin } from 'shared/api/gen/zod.gen';
import Stack from '@mui/material/Stack';
import { useForm, SubmitHandler } from 'react-hook-form';
import SubmitButton from 'shared/ui/SubmitButton';
import { getRouteApi } from '@tanstack/react-router';
import EmailField from 'entities/user/ui/EmailField';
import PasswordField from 'entities/user/ui/PasswordField';
import GoogleAuthorizationButton from 'shared/ui/GoogleAuthorizationButton';
import LinkedInAuthorizationButton from 'shared/ui/LinkedInAuthorizationButton';
import { zodResolver } from '@hookform/resolvers/zod';

const routeApi = getRouteApi('/sign-in');

export default function SignInForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<UserLogin>({
    resolver: zodResolver(zUserLogin),
  });
  const {
    auth: { login },
  } = routeApi.useRouteContext();
  const onSubmit: SubmitHandler<UserLogin> = async (data, event) => {
    event?.preventDefault();
    await login(data).catch((err) => {
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
      <SubmitButton isSubmitting={isSubmitting}>Sign In</SubmitButton>
      <GoogleAuthorizationButton />
      <LinkedInAuthorizationButton />
    </Form>
  );
}

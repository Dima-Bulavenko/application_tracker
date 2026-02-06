import { Form } from 'shared/ui/Form';
import { FormError } from 'shared/ui/FormError';
import type { UserCreate } from 'shared/api/gen/types.gen';
import { createUser } from 'shared/api/gen/sdk.gen';
import { zUserCreate } from 'shared/api/gen/zod.gen';
import Stack from '@mui/material/Stack';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { useNavigate } from '@tanstack/react-router';
import EmailField from 'entities/user/ui/EmailField';
import PasswordField from 'entities/user/ui/PasswordField';
import SubmitButton from 'shared/ui/SubmitButton';
import GoogleAuthorizationButton from 'shared/ui/GoogleAuthorizationButton';
import LinkedInAuthorizationButton from 'shared/ui/LinkedInAuthorizationButton';
import { zodResolver } from '@hookform/resolvers/zod';

export default function RegisterForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<UserCreate>({ resolver: zodResolver(zUserCreate) });

  const navigate = useNavigate();

  const onSubmit: SubmitHandler<UserCreate> = async (data, event) => {
    event?.preventDefault();
    const res = await createUser({ body: data });
    if (res.status === 201) {
      navigate({
        to: '/registration-success',
        search: { registrationEmail: data.username },
        replace: true,
      });
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
      <SubmitButton isSubmitting={isSubmitting}>Sign Up</SubmitButton>
      <GoogleAuthorizationButton />
      <LinkedInAuthorizationButton />
    </Form>
  );
}

import { Form, FormError } from 'shared/ui';
import { zUserCreate, type UserCreate, createUser } from 'shared/api';
import { Button, Stack } from '@mui/material';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { customZodResolver } from 'shared/lib';
import { useNavigate } from 'react-router-dom';
import { EmailField, PasswordField } from 'entities/user/ui';

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
      navigate('/sign-in', { replace: true });
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

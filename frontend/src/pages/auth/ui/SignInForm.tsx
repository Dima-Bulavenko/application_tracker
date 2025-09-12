import { Form, FormError } from 'shared/ui';
import { UserLogin, zUserLogin, login } from 'shared/api';
import { Button, Stack } from '@mui/material';
import { useSession } from 'shared/hooks';
import { useForm, SubmitHandler } from 'react-hook-form';
import { customZodResolver } from 'shared/lib';
import { useNavigate } from 'react-router-dom';
import { EmailField, PasswordField } from 'entities/user/ui';

export default function SignInForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<UserLogin>({
    resolver: customZodResolver(zUserLogin),
  });
  const navigate = useNavigate();
  const { setToken } = useSession();
  const onSubmit: SubmitHandler<UserLogin> = async (data, event) => {
    event?.preventDefault();
    const res = await login({ body: data });
    if (res.status === 200) {
      setToken(res.data?.access_token);
      navigate('/dashboard', { replace: true });
    }
    if (res.status === 401) {
      setError('root', { message: 'Invalid email or password' });
    }
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

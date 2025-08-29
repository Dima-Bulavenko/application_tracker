import { Form, TextInput, PasswordInput, FormError } from 'shared/ui';
import { zUserCreate, type UserCreate, createUser } from 'shared/api';
import { Button, Stack } from '@mui/material';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { customZodResolver } from 'shared/lib';
import { useNavigate } from 'react-router-dom';

const passwordHelp = zUserCreate.shape.password._def.description;

export default function RegisterForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { isSubmitting, errors },
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
        <TextInput
          name='username'
          type='email'
          label='Email'
          control={control}
          required
          rules={{ required: true }}
          disabled={isSubmitting}
        />
        <PasswordInput
          name='password'
          control={control}
          required
          disabled={isSubmitting}
          rules={{ required: true }}
          helperText={passwordHelp}
        />
      </Stack>
      <FormError message={errors.root?.message} />
      <Button sx={{ mt: 5 }} type='submit' color='primary' variant='contained'>
        Sign Up
      </Button>
    </Form>
  );
}

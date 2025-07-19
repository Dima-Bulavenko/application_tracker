import { useForm, SubmitHandler } from 'react-hook-form';
import { zUserCreate } from '../client/zod.gen';
import { UserCreate } from '../client/types.gen';
import { createUserUsersPost } from '../client/sdk.gen';
import { customZodResolver } from '../utils/customZodResolver';
import PasswordInput from './PasswordInput';
import BaseInput from './BaseInput';
import { BaseForm } from './BaseForm';

export default function Register() {
  const { control, handleSubmit } = useForm<UserCreate>({
    resolver: customZodResolver(zUserCreate),
  });

  const onSubmit: SubmitHandler<UserCreate> = async (data, event) => {
    event?.preventDefault();
    createUserUsersPost({ body: data })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <BaseForm onSubmit={handleSubmit(onSubmit)} submitText='Sign up'>
      <BaseInput name='email' type='email' control={control} required />
      <PasswordInput name='password' control={control} required />
    </BaseForm>
  );
}

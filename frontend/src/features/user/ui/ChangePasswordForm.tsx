import PasswordField from 'entities/user/ui/PasswordField';
import { type SubmitHandler, useForm } from 'react-hook-form';
import { changePassword } from 'shared/api/gen';
import { zUserChangePassword } from 'shared/api/gen/zod.gen';
import { Form } from 'shared/ui/Form';
import z from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import Stack from '@mui/material/Stack';
import SubmitButton from 'shared/ui/SubmitButton';
import { FormError } from 'shared/ui/FormError';

type FormType = z.infer<typeof zUserChangePassword>;

// Extend schema to validate password confirmation
const passwordHelperText =
  'Password must be 8 characters long, contain at least one uppercase letter and one number.';
const zPasswordFiled = z
  .string(passwordHelperText)
  .regex(/^(?=.*[A-Z])(?=.*\d).{8,}$/, passwordHelperText);

const validationSchema = z
  .object({
    old_password: zPasswordFiled,
    new_password: zPasswordFiled,
    confirm_new_password: zPasswordFiled,
  })
  .refine((data) => data.new_password === data.confirm_new_password, {
    message: "Passwords don't match",
    path: ['confirm_new_password'],
  });

export function ChangePasswordForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { isSubmitting, errors },
  } = useForm<FormType>({
    resolver: zodResolver(validationSchema),
    defaultValues: {
      old_password: '',
      new_password: '',
      confirm_new_password: '',
    },
  });

  const onSubmit: SubmitHandler<FormType> = async (data, event) => {
    event?.preventDefault();
    const response = await changePassword<false>({
      body: data,
      throwOnError: false,
    });
    if (response.status === 200) return;
    if (response.status === 400)
      return setError('old_password', {
        message: 'Current password is incorrect',
      });
    if (response.status === 422 && Array.isArray(response.error?.detail)) {
      response.error.detail.forEach((err) => {
        const fieldName = err.loc[err.loc.length - 1];
        if (typeof fieldName === 'string' && fieldName in data) {
          setError(fieldName as keyof FormType, { message: err.msg });
        }
      });
      return;
    }
    setError('root', {
      message:
        'An unexpected error occurred. Please reload page or try again later.',
    });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <PasswordField
          name='old_password'
          control={control}
          label='Current Password'
          helperText={passwordHelperText}
        />
        <PasswordField
          name='new_password'
          control={control}
          label='New Password'
          helperText=''
        />
        <PasswordField
          name='confirm_new_password'
          control={control}
          label='Confirm New Password'
          helperText=''
        />
      </Stack>
      <FormError message={errors.root?.message} />
      <SubmitButton isSubmitting={isSubmitting}>
        Create Application
      </SubmitButton>
    </Form>
  );
}

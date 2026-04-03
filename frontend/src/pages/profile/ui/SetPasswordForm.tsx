import { zodResolver } from '@hookform/resolvers/zod'
import PasswordField from 'entities/user/ui/PasswordField'
import { type SubmitHandler, useForm } from 'react-hook-form'
import { setPassword } from 'shared/api/gen'
import { zUserSetPassword } from 'shared/api/gen/zod.gen'
import { Form } from 'shared/ui/Form'
import { FormError } from 'shared/ui/FormError'
import SubmitButton from 'shared/ui/SubmitButton'
import { toast } from 'sonner'
import z from 'zod'

type FormType = z.infer<typeof zUserSetPassword>

// Extend schema to validate password confirmation
const passwordHelperText =
  'Password must be 8 characters long, contain at least one uppercase letter and one number.'
const zPasswordFiled = z
  .string(passwordHelperText)
  .regex(/^(?=.*[A-Z])(?=.*\d).{8,}$/, passwordHelperText)

const validationSchema = z
  .object({
    new_password: zPasswordFiled,
    confirm_new_password: zPasswordFiled,
  })
  .refine((data) => data.new_password === data.confirm_new_password, {
    message: "Passwords don't match",
    path: ['confirm_new_password'],
  })

type SetPasswordForm = {
  onSuccess?: () => void
}

export function SetPasswordForm({ onSuccess }: SetPasswordForm) {
  const {
    control,
    handleSubmit,
    setError,
    formState: { isSubmitting, errors },
  } = useForm<FormType>({
    resolver: zodResolver(validationSchema),
    defaultValues: {
      new_password: '',
      confirm_new_password: '',
    },
  })

  const onSubmit: SubmitHandler<FormType> = async (data, event) => {
    event?.preventDefault()
    const response = await setPassword<false>({
      body: data,
      throwOnError: false,
    })
    if (response.status === 200) {
      toast.success('Password set successfully')
      return onSuccess?.()
    }
    if (response.status === 422 && Array.isArray(response.error?.detail)) {
      response.error.detail.forEach((err) => {
        const fieldName = err.loc[err.loc.length - 1]
        if (typeof fieldName === 'string' && fieldName in data) {
          setError(fieldName as keyof FormType, { message: err.msg })
        }
      })
      return
    }
    setError('root', {
      message:
        'An unexpected error occurred. Please reload page or try again later.',
    })
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <div className='space-y-2'>
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
      </div>
      <FormError message={errors.root?.message} />
      <SubmitButton isSubmitting={isSubmitting}>Set Password</SubmitButton>
    </Form>
  )
}

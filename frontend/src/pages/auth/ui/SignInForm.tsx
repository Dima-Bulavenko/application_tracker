import { zodResolver } from '@hookform/resolvers/zod'
import { getRouteApi } from '@tanstack/react-router'
import EmailField from 'entities/user/ui/EmailField'
import PasswordField from 'entities/user/ui/PasswordField'
import { type SubmitHandler, useForm } from 'react-hook-form'
import type { UserLogin } from 'shared/api/gen/types.gen'
import { zUserLogin } from 'shared/api/gen/zod.gen'
import { Form } from 'shared/ui/Form'
import { FormError } from 'shared/ui/FormError'
import GoogleAuthorizationButton from 'shared/ui/GoogleAuthorizationButton'
import LinkedInAuthorizationButton from 'shared/ui/LinkedInAuthorizationButton'
import SubmitButton from 'shared/ui/SubmitButton'

const routeApi = getRouteApi('/sign-in')

export default function SignInForm() {
  const {
    control,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<UserLogin>({
    resolver: zodResolver(zUserLogin),
    defaultValues: {
      username: '',
      password: '',
    },
  })
  const {
    auth: { login },
  } = routeApi.useRouteContext()
  const onSubmit: SubmitHandler<UserLogin> = async (data, event) => {
    event?.preventDefault()
    await login(data).catch((err) => {
      if (err.status === 401) {
        setError('root', { message: 'Invalid email or password' })
      }
    })
  }
  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <div className='space-y-5'>
        <EmailField name='username' control={control} />
        <PasswordField name='password' control={control} />
      </div>
      <FormError message={errors.root?.message} />
      <SubmitButton isSubmitting={isSubmitting}>Sign In</SubmitButton>
      <GoogleAuthorizationButton />
      <LinkedInAuthorizationButton />
    </Form>
  )
}

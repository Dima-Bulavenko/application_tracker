import { useQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { Loader2 } from 'lucide-react'
import { activateUser } from 'shared/api/gen/sdk.gen'
import { LinkButton } from 'shared/ui/LinkButton'
import { AuthPage } from './AuthPage'

const routeApi = getRouteApi('/verify-email')

export function VerifyEmailPage() {
  const { token } = routeApi.useSearch()

  const { isLoading, isSuccess, isError, error } = useQuery({
    queryKey: ['activateUser', token],
    enabled: !!token,
    retry: false,
    queryFn: () => activateUser({ query: { token } }),
  })

  if (isLoading) {
    return (
      <AuthPage title='Verifying your email...'>
        <div className='flex flex-col items-center gap-3'>
          <Loader2 className='size-8 animate-spin text-muted-foreground' />
          <p className='text-sm text-muted-foreground'>
            Please wait while we confirm your account.
          </p>
        </div>
      </AuthPage>
    )
  }

  if (isSuccess) {
    return (
      <AuthPage
        title='Email verified'
        subtitle='Your account has been activated. You can now sign in.'
        footerText="Don't have an account?"
        footerLinkText='Register'
        footerTo='/register'
      >
        <div className='flex flex-col items-center gap-3'>
          <p className='text-center text-sm text-muted-foreground'>
            Welcome aboard! Use your credentials to access your dashboard.
          </p>
          <LinkButton to='/sign-in'>Go to Sign In</LinkButton>
        </div>
      </AuthPage>
    )
  }

  return (
    <AuthPage
      title='Verification failed'
      subtitle={
        (isError && error?.message) ||
        'We could not verify your email with this link.'
      }
      footerText='Need a new account?'
      footerLinkText='Register'
      footerTo='/register'
    >
      <div className='flex flex-col items-center gap-3'>
        <p className='text-center text-sm text-muted-foreground'>
          You can try signing in or registering again.
        </p>
        <LinkButton to='/sign-in'>Go to Sign In</LinkButton>
      </div>
    </AuthPage>
  )
}

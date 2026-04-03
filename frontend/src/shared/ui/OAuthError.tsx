import { Alert, AlertDescription, AlertTitle } from 'app/components/ui/alert'
import { AlertCircle } from 'lucide-react'
import type { ReactNode } from 'react'
import GoogleAuthorizationButton from './GoogleAuthorizationButton'
import LinkedInAuthorizationButton from './LinkedInAuthorizationButton'

interface OAuthErrorProps {
  authButton: ReactNode
  errorMessage?: string
  provider?: string
}

const providerButtons: Record<string, ReactNode> = {
  google: <GoogleAuthorizationButton action='sign-in' />,
  linkedin: <LinkedInAuthorizationButton action='sign-in' />,
}

export default function OAuthError({
  authButton,
  errorMessage,
  provider,
}: OAuthErrorProps) {
  const buttonToRender = (provider && providerButtons[provider]) || authButton

  return (
    <div className='flex min-h-screen flex-col items-center justify-center p-6'>
      <div className='flex w-full max-w-[500px] flex-col gap-6'>
        <Alert variant='destructive'>
          <AlertCircle className='size-4' />
          <AlertTitle>Authentication Error</AlertTitle>
          <AlertDescription>
            {errorMessage ||
              'An error occurred during authentication. Please try signing in again.'}
          </AlertDescription>
        </Alert>

        <p className='text-center text-sm text-muted-foreground'>
          If the problem persists, please contact support.
        </p>

        {buttonToRender}
      </div>
    </div>
  )
}

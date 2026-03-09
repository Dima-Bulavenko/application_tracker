import { Alert, AlertDescription, AlertTitle } from 'app/components/ui/alert'
import { AlertCircle } from 'lucide-react'
import type { ReactNode } from 'react'

interface OAuthErrorProps {
  authButton: ReactNode
}

export default function OAuthError({ authButton }: OAuthErrorProps) {
  return (
    <div className='flex min-h-screen flex-col items-center justify-center p-6'>
      <div className='flex w-full max-w-[500px] flex-col gap-6'>
        <Alert variant='destructive'>
          <AlertCircle className='size-4' />
          <AlertTitle>Authentication Error</AlertTitle>
          <AlertDescription>
            An error occurred during authentication. Please try signing in
            again.
          </AlertDescription>
        </Alert>

        <p className='text-center text-sm text-muted-foreground'>
          If the problem persists, please contact support.
        </p>

        {authButton}
      </div>
    </div>
  )
}

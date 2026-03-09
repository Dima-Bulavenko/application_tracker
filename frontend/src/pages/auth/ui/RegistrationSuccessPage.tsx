import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from 'app/components/ui/card'
import { Mail } from 'lucide-react'

export function RegistrationSuccessPage() {
  return (
    <div className='flex min-h-dvh items-center justify-center p-3'>
      <Card className='w-full max-w-[500px] text-center'>
        <CardHeader>
          <div className='mb-2 flex justify-center'>
            <Mail className='size-16 text-primary' />
          </div>
          <CardTitle className='text-2xl'>Check Your Email</CardTitle>
        </CardHeader>
        <CardContent className='space-y-3'>
          <p className='text-muted-foreground'>
            We've sent an activation email to your inbox. Please check your
            email and click the activation link to complete your registration.
          </p>
          <div className='rounded-md bg-muted p-4'>
            <p className='text-sm font-semibold'>Didn't receive the email?</p>
            <p className='mt-1 text-sm text-muted-foreground'>
              Try registering again with the same email address to resend the
              activation email.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

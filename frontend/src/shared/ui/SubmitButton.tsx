import { Button } from 'app/components/ui/button'
import { Loader2 } from 'lucide-react'

interface SubmitButtonProps
  extends Omit<React.ComponentProps<typeof Button>, 'type'> {
  isSubmitting: boolean
  children: React.ReactNode
}

export default function SubmitButton({
  isSubmitting,
  children,
  disabled,
  ...props
}: SubmitButtonProps) {
  return (
    <Button
      type='submit'
      disabled={isSubmitting || disabled}
      className='mt-5'
      {...props}
    >
      {isSubmitting ? <Loader2 className='size-5 animate-spin' /> : children}
    </Button>
  )
}

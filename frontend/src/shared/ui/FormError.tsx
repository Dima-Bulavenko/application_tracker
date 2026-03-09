import { AlertCircle } from 'lucide-react'
import type { PropsWithChildren } from 'react'

type FormErrorProps = PropsWithChildren<{
  message?: string
}>

export function FormError({ message, children }: FormErrorProps) {
  const content = message ?? children
  if (!content) return null
  return (
    <div
      role='alert'
      aria-live='polite'
      className='mt-2 flex items-center gap-2 text-destructive'
    >
      <AlertCircle className='size-5 shrink-0' />
      <p className='text-sm'>{content}</p>
    </div>
  )
}

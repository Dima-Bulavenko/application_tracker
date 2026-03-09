import type { LinkComponent } from '@tanstack/react-router'
import { createLink } from '@tanstack/react-router'
import { buttonVariants } from 'app/components/ui/button'
import { cn } from 'app/lib/utils'
import type { VariantProps } from 'class-variance-authority'
import React from 'react'

type ButtonLinkProps = React.ComponentProps<'a'> &
  VariantProps<typeof buttonVariants>

const ButtonLinkComponent = React.forwardRef<
  HTMLAnchorElement,
  ButtonLinkProps
>(({ className, variant, size, ...props }, ref) => (
  <a
    ref={ref}
    className={cn(buttonVariants({ variant, size, className }))}
    {...props}
  />
))

const CreatedButtonLinkComponent = createLink(ButtonLinkComponent)

export const LinkButton: LinkComponent<typeof ButtonLinkComponent> = (
  props
) => {
  return <CreatedButtonLinkComponent preload='intent' {...props} />
}

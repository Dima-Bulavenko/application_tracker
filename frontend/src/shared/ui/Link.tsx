import { createLink } from '@tanstack/react-router'
import { forwardRef } from 'react'

export const Link = createLink(
  forwardRef<HTMLAnchorElement, React.ComponentProps<'a'>>((props, ref) => {
    return <a ref={ref} {...props} />
  })
)

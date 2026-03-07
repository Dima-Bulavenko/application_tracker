// src/components/ui/mui-router-link.tsx

import MuiLink, { type LinkProps } from '@mui/material/Link'
import { createLink } from '@tanstack/react-router'
import { forwardRef } from 'react'

// Create a router-compatible MUI Link with full type safety
export const Link = createLink(
  forwardRef<HTMLAnchorElement, LinkProps>((props, ref) => {
    return <MuiLink ref={ref} {...props} />
  })
)

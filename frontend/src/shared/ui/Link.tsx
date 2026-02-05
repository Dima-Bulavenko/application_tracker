// src/components/ui/mui-router-link.tsx
import { createLink } from '@tanstack/react-router';
import { type LinkProps } from '@mui/material/Link';
import MuiLink from '@mui/material/Link';
import { forwardRef } from 'react';

// Create a router-compatible MUI Link with full type safety
export const Link = createLink(
  forwardRef<HTMLAnchorElement, LinkProps>((props, ref) => {
    return <MuiLink ref={ref} {...props} />;
  })
);

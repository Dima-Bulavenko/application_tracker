import type { ButtonProps } from '@mui/material'
import Button from '@mui/material/Button'
import type { LinkComponent } from '@tanstack/react-router'
import { createLink } from '@tanstack/react-router'
import React from 'react'

type MUIButtonLinkProps = ButtonProps<'a'>

const MUIButtonLinkComponent = React.forwardRef<
  HTMLAnchorElement,
  MUIButtonLinkProps
>((props, ref) => <Button ref={ref} component='a' {...props} />)

const CreatedButtonLinkComponent = createLink(MUIButtonLinkComponent)

export const LinkButton: LinkComponent<typeof MUIButtonLinkComponent> = (
  props
) => {
  return <CreatedButtonLinkComponent preload={'intent'} {...props} />
}

import Button from '@mui/material/Button';
import { Link as RouterLink, type LinkProps } from '@tanstack/react-router';

type AnchorButtonProps = React.ComponentProps<typeof Button<'a'>>;
export type LinkButtonProps = Omit<AnchorButtonProps, 'component' | 'href'> &
  LinkProps;

export function LinkButton(props: LinkButtonProps) {
  return <Button component={RouterLink} {...props} />;
}

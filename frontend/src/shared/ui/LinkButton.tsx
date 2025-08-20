import { Button } from '@mui/material';
import { Link as RouterLink, type LinkProps } from 'react-router-dom';

type AnchorButtonProps = React.ComponentProps<typeof Button<'a'>>;
export type LinkButtonProps = Omit<AnchorButtonProps, 'component' | 'href'> &
  LinkProps;

export function LinkButton(props: LinkButtonProps) {
  return <Button component={RouterLink} {...props} />;
}

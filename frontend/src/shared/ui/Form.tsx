import { Box, BoxProps } from '@mui/material';
import type { Theme } from '@mui/material/styles';
import type { SxProps } from '@mui/system';

type BaseFormProps = Omit<BoxProps<'form'>, 'component'>;

export function Form({ children, sx, ...props }: BaseFormProps) {
  const baseSx = (theme: Theme) => ({
    p: theme.spacing(3),
    m: 'auto',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    maxWidth: theme.spacing(55),
  });
  const mergedSx: SxProps<Theme> = [
    baseSx,
    ...(Array.isArray(sx) ? sx : sx ? [sx] : []),
  ];
  return (
    <Box component='form' noValidate sx={mergedSx} {...props}>
      {children}
    </Box>
  );
}

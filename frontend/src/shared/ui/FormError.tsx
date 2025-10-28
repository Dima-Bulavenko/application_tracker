import Box from '@mui/material/Box';
import type { BoxProps } from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { PropsWithChildren } from 'react';

type FormErrorProps = PropsWithChildren<
  Omit<BoxProps, 'component' | 'children'> & {
    message?: string;
  }
>;

// A compact, inline form error message (smaller than MUI Alert)
export function FormError({ message, children, ...props }: FormErrorProps) {
  const content = message ?? children;
  if (!content) return null;
  return (
    <Box
      role='alert'
      aria-live='polite'
      display='flex'
      alignItems='center'
      gap={1}
      color={(theme) => theme.palette.error.main}
      sx={{ mt: 1 }}
      {...props}>
      <ErrorOutlineIcon fontSize='medium' />
      <Typography variant='caption' sx={{ m: 0 }}>
        {content}
      </Typography>
    </Box>
  );
}

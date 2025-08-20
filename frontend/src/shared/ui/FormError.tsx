import { Box, BoxProps, Typography } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { PropsWithChildren } from 'react';

type FormErrorProps = PropsWithChildren<
  Omit<BoxProps, 'component' | 'children'> & {
    message?: string;
  }
>;

// A compact, inline form error message (smaller than MUI Alert)
export function FormError({ message, children, sx, ...props }: FormErrorProps) {
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
      sx={sx}
      {...props}>
      <ErrorOutlineIcon fontSize='medium' />
      <Typography variant='caption' sx={{ m: 0 }}>
        {content}
      </Typography>
    </Box>
  );
}

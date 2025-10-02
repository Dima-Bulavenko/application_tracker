import { Add as AddIcon } from '@mui/icons-material';
import { Box, IconButton, type ButtonProps } from '@mui/material';

type CreateApplicationButtonProps = ButtonProps;

export function CreateApplicationButton(props: CreateApplicationButtonProps) {
  return (
    <Box
      sx={(theme) => ({
        position: 'fixed',
        bottom: theme.spacing(12),
        right: theme.spacing(2),
        zIndex: theme.zIndex.appBar,
      })}>
      <IconButton
        sx={{ backgroundColor: 'primary.main' }}
        variant='contained'
        size='medium'
        {...props}>
        <AddIcon fontSize='inherit' />
      </IconButton>
    </Box>
  );
}

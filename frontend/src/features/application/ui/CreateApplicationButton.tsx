import { Add as AddIcon } from '@mui/icons-material';
import { Button, type ButtonProps } from '@mui/material';

type CreateApplicationButtonProps = ButtonProps;

export function CreateApplicationButton(props: CreateApplicationButtonProps) {
  return (
    <Button
      startIcon={<AddIcon />}
      variant='contained'
      color='primary'
      {...props}>
      New Application
    </Button>
  );
}

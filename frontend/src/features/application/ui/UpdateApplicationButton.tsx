import EditIcon from '@mui/icons-material/Edit';
import { Button, type ButtonProps } from '@mui/material';

type CreateApplicationButtonProps = ButtonProps;

export function UpdateApplicationButton(props: CreateApplicationButtonProps) {
  return (
    <Button
      startIcon={<EditIcon />}
      variant='contained'
      color='primary'
      {...props}
    />
  );
}

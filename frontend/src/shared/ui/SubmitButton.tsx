import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import type { ButtonProps } from '@mui/material/Button';

interface SubmitButtonProps extends Omit<ButtonProps, 'type'> {
  isSubmitting: boolean;
  children: React.ReactNode;
}

export default function SubmitButton({
  isSubmitting,
  children,
  disabled,
  ...props
}: SubmitButtonProps) {
  return (
    <Button
      sx={{ mt: 5 }}
      color='primary'
      variant='contained'
      type='submit'
      disabled={isSubmitting || disabled}
      {...props}>
      {isSubmitting ? <CircularProgress size={24} /> : children}
    </Button>
  );
}

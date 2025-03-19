import { Box, BoxProps, Button } from '@mui/material';

type BaseFormProps = BoxProps & {
  submitText: string;
};

export function BaseForm({ children, submitText, ...props }: BaseFormProps) {
  return (
    <Box
      component='form'
      noValidate
      sx={(theme) => ({
        p: theme.spacing(3),
        m: 'auto',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        gap: theme.spacing(4),
        maxWidth: theme.spacing(55),
      })}
      {...props}>
      {children}
      <Button type='submit' variant='contained' size='large'>
        {submitText}
      </Button>
    </Box>
  );
}

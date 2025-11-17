import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import { UpdateForm } from 'features/user/ui/UpdateForm';

export function PersonalInfoSection() {
  return (
    <Paper elevation={1} sx={{ p: 3 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant='h6' component='h2' gutterBottom>
          Personal Information
        </Typography>
        <Typography variant='body2' color='text.secondary'>
          Update your name and personal details
        </Typography>
      </Box>
      <UpdateForm />
    </Paper>
  );
}

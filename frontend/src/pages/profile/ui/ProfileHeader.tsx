import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import PersonIcon from '@mui/icons-material/Person';

export function ProfileHeader() {
  return (
    <Box>
      <Typography
        variant='h4'
        component='h1'
        gutterBottom
        sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <PersonIcon fontSize='large' />
        Profile Settings
      </Typography>
      <Typography variant='body2' color='text.secondary'>
        Manage your account information and preferences
      </Typography>
    </Box>
  );
}

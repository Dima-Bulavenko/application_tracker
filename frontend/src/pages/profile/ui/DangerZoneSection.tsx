import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import { DeleteAccountButton } from 'features/user/ui/DeleteAccountButton';

export function DangerZoneSection() {
  return (
    <Paper
      elevation={1}
      sx={{
        p: 3,
        borderColor: 'error.main',
        borderWidth: 1,
        borderStyle: 'solid',
        bgcolor: (theme) =>
          theme.palette.mode === 'dark'
            ? 'rgba(211, 47, 47, 0.05)'
            : 'rgba(211, 47, 47, 0.02)',
      }}>
      <Box sx={{ mb: 5 }}>
        <Typography
          variant='h6'
          component='h2'
          gutterBottom
          color='error'
          sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <WarningAmberIcon />
          Danger Zone
        </Typography>
        <Typography variant='body2' color='text.secondary'>
          Permanently delete your account and all associated data
        </Typography>
      </Box>
      <DeleteAccountButton />
    </Paper>
  );
}

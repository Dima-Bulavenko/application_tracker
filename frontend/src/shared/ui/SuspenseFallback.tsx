import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

export function SuspenseFallback() {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        height: '100%',
        minHeight: '200px',
      }}>
      <CircularProgress />
    </Box>
  );
}

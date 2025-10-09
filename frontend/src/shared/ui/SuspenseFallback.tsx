import { Box, CircularProgress } from '@mui/material';

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

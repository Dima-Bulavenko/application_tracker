import { Box, CircularProgress, Stack, Typography } from '@mui/material';
import { useApplicationsList } from 'entities/application/api';
import ApplicationCard from 'entities/application/ui/ApplicationCard';

export function ApplicationList(
  params: Parameters<typeof useApplicationsList>[0]
) {
  const { data, isFetching, error } = useApplicationsList({
    ...params,
  });

  if (error) {
    return (
      <Box display='flex' flexDirection='column' alignItems='center' gap={1}>
        <Typography color='error' variant='body2'>
          {error.message}
        </Typography>
      </Box>
    );
  }

  if (!isFetching && data?.length === 0) {
    return (
      <Typography variant='body2' color='text.secondary'>
        No applications yet.
      </Typography>
    );
  }

  return (
    <Stack spacing={2}>
      {data?.map((app) => <ApplicationCard key={app.id} application={app} />)}

      {isFetching && (
        <Box display='flex' justifyContent='center' py={1}>
          <CircularProgress size={24} />
        </Box>
      )}
    </Stack>
  );
}

export default ApplicationList;

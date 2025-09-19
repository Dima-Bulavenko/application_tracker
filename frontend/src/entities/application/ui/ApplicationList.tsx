import { Box, CircularProgress, Stack, Typography } from '@mui/material';
import { type useApplicationsList } from 'entities/application/api';
import ApplicationCard from 'entities/application/ui/ApplicationCard';

type Prop = {
  queryResult: ReturnType<typeof useApplicationsList>;
};

export function ApplicationList({ queryResult }: Prop) {
  const { error, isFetching, data } = queryResult;

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

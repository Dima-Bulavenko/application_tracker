import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { type useApplicationsList } from 'entities/application/api/useApplications';
import ApplicationCard from './ApplicationCard';
import ApplicationCardSkeleton from './ApplicationCardSkeleton';

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

  if (isFetching) {
    return (
      <Stack spacing={2}>
        {Array.from({ length: 5 }).map((_, index) => (
          <ApplicationCardSkeleton key={index} />
        ))}
      </Stack>
    );
  }

  return (
    <Stack spacing={2}>
      {data?.map((app) => <ApplicationCard key={app.id} application={app} />)}
    </Stack>
  );
}

export default ApplicationList;

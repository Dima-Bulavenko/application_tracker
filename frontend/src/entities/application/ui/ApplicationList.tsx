import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { applicationsOptions } from 'entities/application/api/queryOptions';
import ApplicationCard from './ApplicationCard';
import ApplicationCardSkeleton from './ApplicationCardSkeleton';
import { useSuspenseQuery } from '@tanstack/react-query';
import { getRouteApi } from '@tanstack/react-router';

const routeApi = getRouteApi('/_authenticated/dashboard');

export function ApplicationList() {
  const { filter } = routeApi.useSearch();
  const { error, isFetching, data } = useSuspenseQuery(
    applicationsOptions(filter)
  );

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

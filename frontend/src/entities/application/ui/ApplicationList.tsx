import { Box, Stack, Typography } from '@mui/material';
import { type useApplicationsList } from 'entities/application/api';
import {
  ApplicationCard,
  ApplicationCardSkeleton,
} from 'entities/application/ui';

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

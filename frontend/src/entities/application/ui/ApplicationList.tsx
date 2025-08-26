import {
  Box,
  Button,
  CircularProgress,
  Stack,
  Typography,
} from '@mui/material';
import { useApplications } from 'entities/application/api/useApplications';
import ApplicationCard from 'entities/application/ui/ApplicationCard';

type Props = {
  pageSize?: number;
};

export function ApplicationList({ pageSize = 10 }: Props) {
  const { items, loading, error, hasMore, loadMore, refetch } = useApplications(
    { pageSize, orderBy: 'time_update', orderDirection: 'desc' }
  );

  if (error) {
    return (
      <Box display='flex' flexDirection='column' alignItems='center' gap={1}>
        <Typography color='error' variant='body2'>
          {error}
        </Typography>
        <Button size='small' variant='outlined' onClick={refetch}>
          Retry
        </Button>
      </Box>
    );
  }

  if (!loading && items.length === 0) {
    return (
      <Typography variant='body2' color='text.secondary'>
        No applications yet.
      </Typography>
    );
  }

  return (
    <Stack spacing={2}>
      {items.map((app) => (
        <ApplicationCard key={app.id} application={app} />
      ))}

      {loading && (
        <Box display='flex' justifyContent='center' py={1}>
          <CircularProgress size={24} />
        </Box>
      )}

      {!loading && hasMore && (
        <Box display='flex' justifyContent='center'>
          <Button variant='outlined' onClick={loadMore}>
            Load more
          </Button>
        </Box>
      )}
    </Stack>
  );
}

export default ApplicationList;

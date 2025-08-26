import {
  Card,
  CardContent,
  CardHeader,
  Chip,
  Divider,
  Stack,
  Typography,
} from '@mui/material';
import type { ApplicationReadWithCompany as ApplicationRead } from 'shared/api/gen/types.gen';
import { formatDate } from 'shared/lib';
import {
  humanizeWorkLocation,
  humanizeWorkType,
} from 'entities/application/lib/humanize';
import { statusColor } from 'entities/application/lib/status';

type Props = { application: ApplicationRead };

export function ApplicationCard({ application }: Props) {
  const {
    role,
    status,
    work_location,
    work_type,
    interview_date,
    time_create,
    time_update,
    company,
  } = application;

  return (
    <Card variant='outlined' sx={{ maxWidth: 720 }}>
      <CardHeader
        title={role}
        subheader={`${company.name}`}
        slotProps={{ title: { fontWeight: 600 } }}
      />
      <CardContent>
        <Stack direction='row' spacing={1} flexWrap='wrap' useFlexGap>
          {status && (
            <Chip
              size='small'
              label={`Status: ${status}`}
              color={statusColor[status]}
            />
          )}
          {work_type && (
            <Chip
              size='small'
              label={humanizeWorkType(work_type)}
              variant='outlined'
            />
          )}
          {work_location && (
            <Chip
              size='small'
              label={humanizeWorkLocation(work_location)}
              variant='outlined'
            />
          )}
          {interview_date && (
            <Chip
              size='small'
              label={`Interview: ${formatDate(interview_date)}`}
              variant='outlined'
            />
          )}
        </Stack>

        {(time_create || time_update) && <Divider sx={{ my: 1.5 }} />}

        {(time_create || time_update) && (
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={1}
            divider={<Divider orientation='vertical' flexItem />}>
            {time_create && (
              <Typography variant='caption' color='text.secondary'>
                Created: {formatDate(time_create)}
              </Typography>
            )}
            {time_update && (
              <Typography variant='caption' color='text.secondary'>
                Updated: {formatDate(time_update)}
              </Typography>
            )}
          </Stack>
        )}
      </CardContent>
    </Card>
  );
}

export default ApplicationCard;

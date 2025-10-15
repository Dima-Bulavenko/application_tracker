import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import type { ApplicationReadWithCompany as ApplicationRead } from 'shared/api/gen/types.gen';
import { formatDate } from 'shared/lib/date';
import { humanizeWorkLocation } from 'entities/application/lib/humanize';
import { humanizeWorkType } from 'entities/application/lib/humanize';
import { statusColor } from 'entities/application/lib/status';
import { UpdateApplication } from 'features/application/ui/UpdateApplication';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import { useDeleteApplication } from 'entities/application/api/useApplications';

type Props = { application: ApplicationRead };

function DeleteApplicationButton({
  application_id,
}: {
  application_id: number;
}) {
  const { mutate: deleteApp, isPending } = useDeleteApplication(application_id);
  return (
    <Button
      variant='contained'
      color='error'
      onClick={() => deleteApp()}
      disabled={isPending}>
      <DeleteForeverIcon />
    </Button>
  );
}

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
        <UpdateApplication application={application} />
        <DeleteApplicationButton application_id={application.id} />
      </CardContent>
    </Card>
  );
}

export default ApplicationCard;

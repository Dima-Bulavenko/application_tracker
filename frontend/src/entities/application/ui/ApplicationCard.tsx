import { useMutation } from '@tanstack/react-query'
import { Badge } from 'app/components/ui/badge'
import { Button } from 'app/components/ui/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from 'app/components/ui/card'
import { Separator } from 'app/components/ui/separator'
import { applicationDeleteOptions } from 'entities/application/api/queryOptions'
import {
  humanizeWorkLocation,
  humanizeWorkType,
} from 'entities/application/lib/humanize'
import { statusColor } from 'entities/application/lib/status'
import { UpdateApplication } from 'features/application/ui/UpdateApplication'
import { Trash2 } from 'lucide-react'
import type { ApplicationReadWithCompany as ApplicationRead } from 'shared/api/gen/types.gen'
import { formatDate } from 'shared/lib/date'

type Props = { application: ApplicationRead }

function DeleteApplicationButton({
  application_id,
}: {
  application_id: number
}) {
  const { mutate: deleteApp, isPending } = useMutation(
    applicationDeleteOptions(application_id)
  )
  return (
    <Button
      variant='destructive'
      size='icon'
      onClick={() => deleteApp()}
      disabled={isPending}
    >
      <Trash2 className='size-4' />
    </Button>
  )
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
  } = application
  return (
    <Card className='max-w-[720px]'>
      <CardHeader>
        <CardTitle>{role}</CardTitle>
        <p className='text-sm text-muted-foreground'>{company.name}</p>
      </CardHeader>
      <CardContent className='space-y-3'>
        <div className='flex flex-wrap gap-2'>
          {status && (
            <Badge className={statusColor[status]}>Status: {status}</Badge>
          )}
          {work_type && (
            <Badge variant='outline'>{humanizeWorkType(work_type)}</Badge>
          )}
          {work_location && (
            <Badge variant='outline'>
              {humanizeWorkLocation(work_location)}
            </Badge>
          )}
          {interview_date && (
            <Badge variant='outline'>
              Interview: {formatDate(interview_date)}
            </Badge>
          )}
        </div>

        {(time_create || time_update) && <Separator />}

        {(time_create || time_update) && (
          <div className='flex flex-col gap-1 sm:flex-row sm:gap-3'>
            {time_create && (
              <span className='text-xs text-muted-foreground'>
                Created: {formatDate(time_create)}
              </span>
            )}
            {time_update && (
              <span className='text-xs text-muted-foreground'>
                Updated: {formatDate(time_update)}
              </span>
            )}
          </div>
        )}

        <div className='flex gap-2'>
          <UpdateApplication application={application} />
          <DeleteApplicationButton application_id={application.id} />
        </div>
      </CardContent>
    </Card>
  )
}

export default ApplicationCard

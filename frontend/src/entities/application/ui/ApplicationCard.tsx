import { useMutation } from '@tanstack/react-query'
import { Badge } from 'app/components/ui/badge'
import { Button } from 'app/components/ui/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from 'app/components/ui/card'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from 'app/components/ui/dropdown-menu'
import { Separator } from 'app/components/ui/separator'
import { applicationDeleteOptions } from 'entities/application/api/queryOptions'
import {
  humanizeWorkLocation,
  humanizeWorkType,
} from 'entities/application/lib/humanize'
import { statusColor } from 'entities/application/lib/status'
import { UpdateApplication } from 'features/application/ui/UpdateApplication'
import { MoreHorizontal, Pencil, Trash2 } from 'lucide-react'
import { useState } from 'react'
import type { ApplicationReadWithCompany as ApplicationRead } from 'shared/api/gen/types.gen'
import { formatDate } from 'shared/lib/date'
import { toast } from 'sonner'

type Props = { application: ApplicationRead }

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

  const [updateOpen, setUpdateOpen] = useState(false)
  const { mutate: deleteApp, isPending } = useMutation(
    applicationDeleteOptions(application.id)
  )

  return (
    <Card className='max-w-150'>
      <CardHeader className='flex flex-row items-start justify-between gap-2'>
        <div>
          <CardTitle>{role}</CardTitle>
          <p className='text-sm text-muted-foreground'>{company.name}</p>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant='ghost' size='icon' className='shrink-0'>
              <MoreHorizontal className='size-5' />
              <span className='sr-only'>Open menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align='center'>
            <DropdownMenuItem onClick={() => setUpdateOpen(true)}>
              <Pencil className='mr-2 size-4' />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem
              variant='destructive'
              onClick={() =>
                deleteApp(undefined, {
                  onSuccess: () => toast.success('Application deleted'),
                })
              }
              disabled={isPending}
            >
              <Trash2 className='mr-2 size-4' />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
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
      </CardContent>

      <UpdateApplication
        application={application}
        open={updateOpen}
        onOpenChange={setUpdateOpen}
      />
    </Card>
  )
}

export default ApplicationCard

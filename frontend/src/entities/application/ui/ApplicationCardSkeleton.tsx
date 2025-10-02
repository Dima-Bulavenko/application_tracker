import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Skeleton,
  Stack,
} from '@mui/material';

export function ApplicationCardSkeleton() {
  return (
    <Card variant='outlined' sx={{ maxWidth: 720 }}>
      <CardHeader
        title={<Skeleton variant='text' width='60%' height={32} />}
        subheader={<Skeleton variant='text' width='40%' height={20} />}
      />
      <CardContent>
        <Stack direction='row' spacing={1} flexWrap='wrap' useFlexGap>
          {/* Status chip skeleton */}
          <Skeleton variant='rounded' width={90} height={24} />
          {/* Work type chip skeleton */}
          <Skeleton variant='rounded' width={80} height={24} />
          {/* Work location chip skeleton */}
          <Skeleton variant='rounded' width={75} height={24} />
          {/* Interview date chip skeleton */}
          <Skeleton variant='rounded' width={120} height={24} />
        </Stack>

        <Divider sx={{ my: 1.5 }} />

        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          spacing={1}
          divider={<Divider orientation='vertical' flexItem />}>
          {/* Created date skeleton */}
          <Skeleton variant='text' width={150} height={16} />
          {/* Updated date skeleton */}
          <Skeleton variant='text' width={150} height={16} />
        </Stack>

        {/* Action buttons skeleton */}
        <Stack direction='row' spacing={1} sx={{ mt: 2 }}>
          <Skeleton variant='rounded' width={100} height={36} />
          <Skeleton variant='rounded' width={56} height={36} />
        </Stack>
      </CardContent>
    </Card>
  );
}

export default ApplicationCardSkeleton;

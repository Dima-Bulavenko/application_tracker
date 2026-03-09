import { Card, CardContent } from 'app/components/ui/card'
import { DeleteAccountButton } from 'features/user/ui/DeleteAccountButton'
import { TriangleAlert } from 'lucide-react'

export function DangerZoneSection() {
  return (
    <Card className='border-destructive bg-destructive/5'>
      <CardContent>
        <div className='mb-5'>
          <h2 className='flex items-center gap-1 text-lg font-semibold text-destructive'>
            <TriangleAlert className='size-5' />
            Danger Zone
          </h2>
          <p className='text-sm text-muted-foreground'>
            Permanently delete your account and all associated data
          </p>
        </div>
        <DeleteAccountButton />
      </CardContent>
    </Card>
  )
}

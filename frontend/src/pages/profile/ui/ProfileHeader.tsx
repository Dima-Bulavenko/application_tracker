import { User } from 'lucide-react'

export function ProfileHeader() {
  return (
    <div>
      <h1 className='flex items-center gap-1 text-2xl font-bold'>
        <User className='size-7' />
        Profile Settings
      </h1>
      <p className='text-sm text-muted-foreground'>
        Manage your account information and preferences
      </p>
    </div>
  )
}

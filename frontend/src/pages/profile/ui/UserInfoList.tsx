import { Separator } from 'app/components/ui/separator'
import type { UserRead } from 'shared/api/gen'

interface UserInfoListProps {
  user: UserRead
}

const INFO_ITEMS = [
  { label: 'Email', getValue: (user: UserRead) => user.username },
  {
    label: 'First Name',
    getValue: (user: UserRead) => user.first_name || 'Not set',
  },
  {
    label: 'Second Name',
    getValue: (user: UserRead) => user.second_name || 'Not set',
  },
] as const

export function UserInfoList({ user }: UserInfoListProps) {
  return (
    <div>
      {INFO_ITEMS.map((item, index) => (
        <div key={item.label}>
          <div className='py-3'>
            <p className='mb-0.5 text-sm text-muted-foreground'>{item.label}</p>
            <p>{item.getValue(user)}</p>
          </div>
          {index < INFO_ITEMS.length - 1 && <Separator />}
        </div>
      ))}
    </div>
  )
}

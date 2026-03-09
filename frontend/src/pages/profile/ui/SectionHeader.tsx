import { Button } from 'app/components/ui/button'
import { Pencil } from 'lucide-react'

interface SectionHeaderProps {
  title: string
  subtitle: string
  onEditClick: () => void
}

export function SectionHeader({
  title,
  subtitle,
  onEditClick,
}: SectionHeaderProps) {
  return (
    <div className='mb-3 flex items-start justify-between'>
      <div>
        <h2 className='text-lg font-semibold'>{title}</h2>
        <p className='text-sm text-muted-foreground'>{subtitle}</p>
      </div>
      <Button variant='outline' size='sm' onClick={onEditClick}>
        <Pencil className='size-4' />
        Edit
      </Button>
    </div>
  )
}

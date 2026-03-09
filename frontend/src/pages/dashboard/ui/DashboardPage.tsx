import { ApplicationListWidget } from 'features/application/ui/ApplicationListWidget'
import { CreateApplication } from 'features/application/ui/CreateApplication'

export function DashboardPage() {
  return (
    <div className='mx-auto max-w-7xl px-4 py-2'>
      <ApplicationListWidget />
      <CreateApplication />
    </div>
  )
}

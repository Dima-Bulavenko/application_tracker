import { ApplicationList } from 'entities/application/ui/ApplicationList'
import { FilterApplication } from './FilterApplication'

export function ApplicationListWidget() {
  return (
    <div className='grid w-full items-start gap-4 md:grid-cols-[1fr_360px]'>
      <ApplicationList />
      <FilterApplication />
    </div>
  )
}

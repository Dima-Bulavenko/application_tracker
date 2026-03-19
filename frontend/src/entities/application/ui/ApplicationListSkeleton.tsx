import ApplicationCardSkeleton from './ApplicationCardSkeleton'

export function ApplicationListSkeleton() {
  return (
    <div className='space-y-4'>
      {Array.from({ length: 5 }).map((_, index) => (
        <ApplicationCardSkeleton key={index} />
      ))}
    </div>
  )
}

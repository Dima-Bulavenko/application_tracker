import { getRouteApi } from '@tanstack/react-router'
import { ChangePasswordSection } from './ChangePasswordSection'
import { DangerZoneSection } from './DangerZoneSection'
import { PersonalInfoSection } from './PersonalInfoSection'
import { ProfileHeader } from './ProfileHeader'
import { SetPasswordSection } from './SetPasswordSection'

const routeApi = getRouteApi('/_authenticated')

export function ProfilePage() {
  const {
    auth: { user },
  } = routeApi.useRouteContext()

  return (
    <div className='mx-auto max-w-3xl space-y-4 px-4 py-4'>
      <ProfileHeader />
      <PersonalInfoSection />
      {user.is_password_set && <ChangePasswordSection />}
      {!user.is_password_set && <SetPasswordSection />}
      <DangerZoneSection />
    </div>
  )
}

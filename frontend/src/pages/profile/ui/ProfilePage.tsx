import Container from '@mui/material/Container'
import Stack from '@mui/material/Stack'
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
    <Container maxWidth='md' sx={{ py: 4 }}>
      <Stack spacing={4}>
        <ProfileHeader />
        <PersonalInfoSection />
        {user.is_password_set && <ChangePasswordSection />}
        {!user.is_password_set && <SetPasswordSection />}
        <DangerZoneSection />
      </Stack>
    </Container>
  )
}

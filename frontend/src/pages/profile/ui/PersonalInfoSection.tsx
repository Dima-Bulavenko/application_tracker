import { getRouteApi } from '@tanstack/react-router'
import { Card, CardContent } from 'app/components/ui/card'
import { useState } from 'react'
import { EditDrawer } from './EditDrawer'
import { SectionHeader } from './SectionHeader'
import { UserInfoList } from './UserInfoList'

const routeApi = getRouteApi('/_authenticated')

export function PersonalInfoSection() {
  const [drawerOpen, setDrawerOpen] = useState(false)
  const {
    auth: { user },
  } = routeApi.useRouteContext()

  const handleOpenDrawer = () => setDrawerOpen(true)
  const handleCloseDrawer = () => setDrawerOpen(false)

  return (
    <>
      <Card>
        <CardContent>
          <SectionHeader
            title='Personal Information'
            subtitle='Your profile details'
            onEditClick={handleOpenDrawer}
          />
          <UserInfoList user={user} />
        </CardContent>
      </Card>

      <EditDrawer open={drawerOpen} onClose={handleCloseDrawer} />
    </>
  )
}

import { Card, CardContent } from 'app/components/ui/card'
import { useState } from 'react'
import { SectionHeader } from './SectionHeader'
import { SetPasswordDrawer } from './SetPasswordDrawer'

export function SetPasswordSection() {
  const [drawerOpen, setDrawerOpen] = useState(false)

  const handleOpenDrawer = () => setDrawerOpen(true)
  const handleCloseDrawer = () => setDrawerOpen(false)

  return (
    <>
      <Card>
        <CardContent>
          <SectionHeader
            title='Set Password'
            subtitle='Create a password for your account'
            onEditClick={handleOpenDrawer}
          />
          <SetPasswordDrawer open={drawerOpen} onClose={handleCloseDrawer} />
        </CardContent>
      </Card>
    </>
  )
}

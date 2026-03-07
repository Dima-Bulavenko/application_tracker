import Paper from '@mui/material/Paper'
import { useState } from 'react'
import { ChangePasswordDrawer } from './ChangePasswordDrawer'
import { SectionHeader } from './SectionHeader'

export function ChangePasswordSection() {
  const [drawerOpen, setDrawerOpen] = useState(false)

  const handleOpenDrawer = () => setDrawerOpen(true)
  const handleCloseDrawer = () => setDrawerOpen(false)

  return (
    <>
      <Paper elevation={1} sx={{ p: 3 }}>
        <SectionHeader
          title='Change Password'
          subtitle='Update your account password'
          onEditClick={handleOpenDrawer}
        />
        <ChangePasswordDrawer open={drawerOpen} onClose={handleCloseDrawer} />
      </Paper>
    </>
  )
}

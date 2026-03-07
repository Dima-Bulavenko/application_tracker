import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
import { useTheme } from '@mui/material/styles'
import Typography from '@mui/material/Typography'
import useMediaQuery from '@mui/material/useMediaQuery'
import { getRouteApi } from '@tanstack/react-router'
import { Suspense } from 'react'
import { getCurrentUser } from 'shared/api/gen'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'
import { SetPasswordForm } from './SetPasswordForm'

interface SetPasswordProps {
  open: boolean
  onClose: () => void
}

const routeApi = getRouteApi('/_authenticated')

export function SetPasswordDrawer({ open, onClose }: SetPasswordProps) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const {
    auth: { setUser },
  } = routeApi.useRouteContext()
  const onSuccess = async () => {
    const { data } = await getCurrentUser()
    setUser(data)
    onClose()
  }

  return (
    <Drawer
      anchor='right'
      open={open}
      onClose={onClose}
      slotProps={{
        root: {
          keepMounted: true,
        },
        paper: {
          sx: {
            width: isMobile ? '85vw' : '500px',
            maxWidth: '500px',
          },
        },
      }}
    >
      <Box sx={{ p: 3, height: '100%' }}>
        <Typography variant='h5' component='h2' gutterBottom>
          Set Password
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Suspense fallback={<SuspenseFallback />}>
          {open && <SetPasswordForm onSuccess={onSuccess} />}
        </Suspense>
      </Box>
    </Drawer>
  )
}

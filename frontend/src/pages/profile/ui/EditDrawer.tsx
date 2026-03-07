import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
import { useTheme } from '@mui/material/styles'
import Typography from '@mui/material/Typography'
import useMediaQuery from '@mui/material/useMediaQuery'
import { UpdateForm } from 'features/user/ui/UpdateForm'
import { Suspense } from 'react'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'

interface EditDrawerProps {
  open: boolean
  onClose: () => void
}

export function EditDrawer({ open, onClose }: EditDrawerProps) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

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
          Edit Personal Information
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Suspense fallback={<SuspenseFallback />}>
          {open && <UpdateForm onSuccess={onClose} />}
        </Suspense>
      </Box>
    </Drawer>
  )
}

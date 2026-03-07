import Box from '@mui/material/Box'
import { ApplicationList } from 'entities/application/ui/ApplicationList'
import { FilterApplication } from './FilterApplication'

export function ApplicationListWidget() {
  return (
    <Box
      sx={{
        width: '100%',
        display: { xs: 'block', md: 'grid' },
        gridTemplateColumns: { md: '1fr 360px' },
        gap: 2,
        alignItems: 'start',
      }}
    >
      <ApplicationList />
      <FilterApplication />
    </Box>
  )
}

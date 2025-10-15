import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import useMediaQuery from '@mui/material/useMediaQuery';
import { Suspense, useState } from 'react';
import FilterAltIcon from '@mui/icons-material/FilterAlt';

import type { FilterForm } from 'entities/application/api/types';
import { lazyImport } from 'shared/lib/lazyLoad';
import { SuspenseFallback } from 'shared/ui/SuspenseFallback';

type Prop = {
  setFilterParams: React.Dispatch<React.SetStateAction<FilterForm>>;
  filterParams: FilterForm;
};

const { FilterApplicationForm } = lazyImport(
  () => import('./FilterApplicationForm'),
  'FilterApplicationForm'
);

export function FilterApplication({ setFilterParams, filterParams }: Prop) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const isMobile = useMediaQuery((theme) => theme.breakpoints.down('md'));

  const filterPanel = (
    <Suspense fallback={<SuspenseFallback />}>
      <FilterApplicationForm
        setFilterParams={setFilterParams}
        defaultValues={filterParams}
      />
    </Suspense>
  );

  return isMobile ? (
    <>
      <Box
        sx={(theme) => ({
          position: 'fixed',
          bottom: theme.spacing(4),
          right: theme.spacing(2),
        })}>
        <IconButton
          sx={{ backgroundColor: 'primary.main' }}
          size='medium'
          onClick={() => setDrawerOpen(true)}>
          <FilterAltIcon fontSize='inherit' />
        </IconButton>
      </Box>
      <Drawer
        anchor='right'
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        ModalProps={{ keepMounted: true }}
        slotProps={{ paper: { sx: { width: '85vw', maxWidth: 420 } } }}>
        {drawerOpen && filterPanel}
      </Drawer>
    </>
  ) : (
    <Box sx={{ position: 'sticky', top: (theme) => theme.spacing(2) }}>
      {filterPanel}
    </Box>
  );
}

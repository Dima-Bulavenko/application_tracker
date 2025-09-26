import { type FilterForm, useApplicationsList } from 'entities/application/api';
import { useState } from 'react';
import { FilterApplication } from './FilterApplication';
import { ApplicationList } from 'entities/application/ui';
import { Box } from '@mui/material';

export function ApplicationListWidget() {
  const [filter, setFilter] = useState<FilterForm>();
  const QueryResult = useApplicationsList(
    { ...filter },
    { enabled: !!filter, staleTime: 30000 }
  );
  return (
    <Box
      sx={{
        width: '100%',
        display: { xs: 'block', md: 'grid' },
        gridTemplateColumns: { md: '1fr 360px' },
        gap: 2,
        alignItems: 'start',
      }}>
      <ApplicationList queryResult={QueryResult} />
      <FilterApplication setFilterParams={setFilter} />
    </Box>
  );
}

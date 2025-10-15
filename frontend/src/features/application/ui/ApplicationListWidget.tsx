import { useApplicationsList } from 'entities/application/api/useApplications';
import type { FilterForm } from 'entities/application/api/types';
import { useState } from 'react';
import { FilterApplication } from './FilterApplication';
import { ApplicationList } from 'entities/application/ui/ApplicationList';
import Box from '@mui/material/Box';

const defaultFilterParams: FilterForm = {
  order_by: 'time_create',
  order_direction: 'desc',
  company_name: null,
  status: [],
  work_type: [],
  work_location: [],
};

const filterParams = JSON.parse(
  localStorage.getItem('appFilters') || JSON.stringify(defaultFilterParams)
);

export function ApplicationListWidget() {
  const [filter, setFilter] = useState<FilterForm>(filterParams);
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
      <FilterApplication setFilterParams={setFilter} filterParams={filter} />
    </Box>
  );
}

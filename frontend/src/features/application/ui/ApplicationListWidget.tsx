import { type FilterForm, useApplicationsList } from 'entities/application/api';
import { useState } from 'react';
import { FilterApplication } from './FilterApplication';
import { ApplicationList } from 'entities/application/ui';
import { Box } from '@mui/material';

const defaultFilterParams: FilterForm = {
  order_by: 'time_create',
  order_direction: 'desc',
  company_name: null,
  status: [],
  work_type: [],
  work_location: [],
};

export function ApplicationListWidget() {
  const filterParams = JSON.parse(
    localStorage.getItem('appFilters') || JSON.stringify(defaultFilterParams)
  );
  const [filter, setFilter] = useState<FilterForm>(filterParams);

  const QueryResult = useApplicationsList({
    ...filter,
  });
  return (
    <Box>
      <FilterApplication
        defaultFilterParams={filter}
        setFilterParams={setFilter}
        queryResult={QueryResult}
      />
      <ApplicationList queryResult={QueryResult} />
    </Box>
  );
}

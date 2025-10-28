import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { useForm, useController, Control } from 'react-hook-form';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { useIsFetching } from '@tanstack/react-query';

import { applicationKeys } from 'entities/application/api/queryOptions';
import CompanyField from 'entities/application/ui/CompanyField';

import { zAppStatus, zWorkLocation, zWorkType } from 'shared/api/gen/zod.gen';
import { MultipleSelectField } from 'shared/ui/SelectField';
import { getRouteApi } from '@tanstack/react-router';
import {
  ApplicationFilter,
  cleanFilterData,
  filterStorage,
} from 'features/application/lib/filterStorage';

type FilterFormParam = {
  control: Control<ApplicationFilter>;
};

const routeApi = getRouteApi('/_authenticated/dashboard');

function OrderBy({ control }: FilterFormParam) {
  const { field } = useController<ApplicationFilter>({
    name: 'order_by',
    control,
  });
  return (
    <FormControl>
      <FormLabel id='applications-order-by-label'>Order By</FormLabel>
      <RadioGroup
        {...field}
        aria-labelledby='applications-order-by-label'
        name='application-order-by'>
        <FormControlLabel
          value='time_create'
          control={<Radio />}
          label='Time Create'
        />
        <FormControlLabel
          value='time_update'
          control={<Radio />}
          label='Time Update'
        />
      </RadioGroup>
    </FormControl>
  );
}

function OrderDirection({ control }: FilterFormParam) {
  const { field } = useController<ApplicationFilter>({
    name: 'order_direction',
    control,
  });
  return (
    <FormControl>
      <FormLabel id='applications-order-direction-label'>
        Order Direction
      </FormLabel>
      <RadioGroup
        {...field}
        aria-labelledby='applications-order-direction-label'
        name='application-order-by'>
        <FormControlLabel value='desc' control={<Radio />} label='Descending' />
        <FormControlLabel value='asc' control={<Radio />} label='Ascending' />
      </RadioGroup>
    </FormControl>
  );
}

function ApplicationStatusField({ control }: FilterFormParam) {
  const options = zAppStatus.options;
  const controller = useController({
    name: 'status',
    control,
  });
  return (
    <MultipleSelectField
      controller={controller}
      options={options}
      label='Status'
    />
  );
}
import { DevTool } from '@hookform/devtools';
function WorkLocationField({ control }: FilterFormParam) {
  const options = zWorkLocation.options;
  const controller = useController({
    name: 'work_location',
    control,
  });
  return (
    <MultipleSelectField
      controller={controller}
      options={options}
      label='Work Location'
    />
  );
}

function WorkTypeField({ control }: FilterFormParam) {
  const options = zWorkType.options;
  const controller = useController({
    name: 'work_type',
    control,
  });
  return (
    <MultipleSelectField
      controller={controller}
      options={options}
      label='Work Type'
    />
  );
}

export function FilterApplicationForm() {
  const { filter } = routeApi.useSearch();
  const navigate = routeApi.useNavigate();
  const { control, handleSubmit, formState, reset } =
    useForm<ApplicationFilter>({
      defaultValues: filter,
    });

  const isFetching = useIsFetching({ queryKey: applicationKeys.lists() });

  const applyFilter = (data: ApplicationFilter): void => {
    const cleanedFilters = cleanFilterData(data);
    const hasActiveFilters = Object.keys(cleanedFilters).length > 0;

    filterStorage.save(cleanedFilters);
    navigate({
      search: () => (hasActiveFilters ? { filter: cleanedFilters } : {}),
    });
  };

  const clearFilters = (): void => {
    filterStorage.clear();
    reset({});
    navigate({ search: () => ({}) });
  };

  const hasActiveFilters = Boolean(filter);

  return (
    <Stack spacing={3} sx={{ p: 2 }}>
      <Box>
        <OrderBy control={control} />
        <OrderDirection control={control} />
      </Box>
      <ApplicationStatusField control={control} />
      <WorkLocationField control={control} />
      <WorkTypeField control={control} />
      <CompanyField control={control} name='company_name' />
      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
        <Button
          disabled={!formState.isDirty && !hasActiveFilters}
          onClick={clearFilters}
          type='button'
          variant='outlined'
          color='secondary'>
          Clear Filters
        </Button>
        <Button
          loading={!!isFetching}
          disabled={!formState.isDirty}
          onClick={handleSubmit(applyFilter)}
          type='button'
          variant='contained'
          color='primary'>
          Apply Filters
        </Button>
      </Box>
      <DevTool control={control} placement='bottom-left' />
    </Stack>
  );
}

import {
  Box,
  Button,
  Drawer,
  Stack,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { useForm, useController } from 'react-hook-form';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { useIsFetching } from '@tanstack/react-query';

import { applicationKeys, type FilterForm } from 'entities/application/api';
import { CompanyField } from 'entities/application/ui';

import { zAppStatus, zWorkLocation, zWorkType } from 'shared/api';
import { MultipleSelectField } from 'shared/ui';
import { useEffect, useState } from 'react';
import FilterAltIcon from '@mui/icons-material/FilterAlt';

type FilterFormParam = {
  control: NonNullable<Parameters<typeof useController>[0]['control']>;
};

type Prop = {
  setFilterParams: React.Dispatch<React.SetStateAction<FilterForm | undefined>>;
};

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

function OrderBy({ control }: FilterFormParam) {
  const { field } = useController<FilterForm>({
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
  const { field } = useController<FilterForm>({
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

function FilterForm({ setFilterParams }: Prop) {
  const { control, handleSubmit, reset, formState } = useForm<FilterForm>({
    defaultValues: filterParams,
  });

  useEffect(() => setFilterParams(filterParams), [setFilterParams]);
  const applyFilter = (data: FilterForm) => {
    localStorage.setItem('appFilters', JSON.stringify(data));
    setFilterParams(data);
    reset(data);
  };

  const isFetching = useIsFetching({ queryKey: applicationKeys.lists() });
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
          loading={!!isFetching}
          disabled={!formState.isDirty}
          onClick={handleSubmit(applyFilter)}
          type='button'
          variant='contained'
          color='primary'>
          Apply Filters
        </Button>
      </Box>
    </Stack>
  );
}

export function FilterApplication({ setFilterParams }: Prop) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const filterPanel = <FilterForm setFilterParams={setFilterParams} />;
  return isMobile ? (
    <>
      <Box
        sx={{
          position: 'fixed',
          bottom: theme.spacing(2),
          right: theme.spacing(2),
        }}>
        <Button variant='contained' onClick={() => setDrawerOpen(true)}>
          <FilterAltIcon />
        </Button>
      </Box>
      <Drawer
        anchor='right'
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        ModalProps={{ keepMounted: true }}
        slotProps={{ paper: { sx: { width: '85vw', maxWidth: 420 } } }}>
        {filterPanel}
      </Drawer>
    </>
  ) : (
    <Box sx={{ position: 'sticky', top: (theme) => theme.spacing(2) }}>
      {filterPanel}
    </Box>
  );
}

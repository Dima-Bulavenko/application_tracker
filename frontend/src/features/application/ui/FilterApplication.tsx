import { Box, Button } from '@mui/material';
import { useForm, useController } from 'react-hook-form';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { DevTool } from '@hookform/devtools';
import {
  type AppListQueryRes,
  type FilterForm,
} from 'entities/application/api';

type FilterFormParam = {
  control: NonNullable<Parameters<typeof useController>[0]['control']>;
};

type Prop = {
  defaultFilterParams: FilterForm;
  setFilterParams: React.Dispatch<React.SetStateAction<FilterForm>>;
  queryResult: AppListQueryRes;
};

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

export function FilterApplication({
  queryResult,
  defaultFilterParams,
  setFilterParams,
}: Prop) {
  const { control, handleSubmit, reset, formState } = useForm<FilterForm>({
    defaultValues: defaultFilterParams,
  });

  const { isFetching } = queryResult;
  const applyFilter = (data: FilterForm) => {
    localStorage.setItem('appFilters', JSON.stringify(data));
    setFilterParams(data);
    reset(data);
  };
  return (
    <Box>
      <OrderBy control={control} />
      <OrderDirection control={control} />
      <DevTool control={control} />
      <Button
        loading={isFetching}
        disabled={!formState.isDirty}
        onClick={handleSubmit(applyFilter)}
        type='button'
        variant='contained'
        color='primary'>
        Apply Filters
      </Button>
    </Box>
  );
}

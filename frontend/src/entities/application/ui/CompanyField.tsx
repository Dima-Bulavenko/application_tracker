import React, { useState } from 'react';
import { useController } from 'react-hook-form';
import { type FieldComponent } from 'shared/types/form';
import CircularProgress from '@mui/material/CircularProgress';
import Autocomplete from '@mui/material/Autocomplete';
import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { getUserCompanies } from 'shared/api/gen/sdk.gen';
import { TextInput } from 'shared/ui/TextInput';
import { useDebouncedCallback } from '@tanstack/react-pacer/debouncer';

const CompanyField: FieldComponent = ({ label = 'Company', ...props }) => {
  const controller = useController(props);
  const [open, setOpen] = useState(false);
  const { field } = controller;

  const debouncedFetching = useDebouncedCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = e.target.value;
      field.onChange(val.trim() === '' ? null : val);
    },
    { wait: 400 }
  );
  const { data = [], isFetching } = useQuery({
    queryKey: ['companies', field.value],
    queryFn: async ({ queryKey }) => {
      const response = await getUserCompanies<true>({
        query: { limit: 30, name_contains: queryKey[1] },
      });
      return response.data;
    },
    placeholderData: keepPreviousData,
    enabled: open,
    staleTime: 30000,
  });
  return (
    <Autocomplete
      options={data?.map((c) => c.name)}
      open={open}
      freeSolo
      onChange={(_, value) => {
        field.onChange(value);
      }}
      onOpen={() => setOpen(true)}
      onClose={() => setOpen(false)}
      loading={isFetching}
      value={field.value || ''}
      renderInput={(params) => (
        <TextInput
          {...params}
          label={label}
          controller={controller}
          onChange={debouncedFetching}
          slotProps={{
            input: {
              ...params.InputProps,
              endAdornment: (
                <>
                  {isFetching ? (
                    <CircularProgress color='inherit' size={20} />
                  ) : null}
                  {params.InputProps.endAdornment}
                </>
              ),
            },
          }}
        />
      )}
    />
  );
};

export default CompanyField;

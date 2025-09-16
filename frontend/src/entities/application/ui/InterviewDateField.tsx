import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { useController } from 'react-hook-form';
import { FieldComponent } from 'shared/types';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs from 'dayjs';

const InterviewDateField: FieldComponent = ({
  label = 'Interview date',
  ...props
}) => {
  const { field, fieldState } = useController(props);
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DateTimePicker
        label={label}
        name={field.name}
        inputRef={field.ref}
        value={dayjs(field.value)}
        onChange={(value) => {
          field.onChange(value?.toISOString() ?? null);
        }}
        slotProps={{
          actionBar: { actions: ['clear', 'cancel', 'accept'] },
          textField: {
            helperText: fieldState.error?.message
              ? fieldState.error.message
              : '',
            error: !!fieldState.error,
          },
        }}
      />
    </LocalizationProvider>
  );
};

export default InterviewDateField;

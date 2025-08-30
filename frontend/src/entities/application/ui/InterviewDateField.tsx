import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { useController } from 'react-hook-form';
import { FieldComponent } from 'shared/types';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

const InterviewDateField: FieldComponent = ({
  label = 'Interview date',
  ...props
}) => {
  const { field } = useController(props);
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DateTimePicker
        label={label}
        name={field.name}
        ref={field.ref}
        onChange={(value) => {
          field.onChange(value?.toISOString());
        }}
      />
    </LocalizationProvider>
  );
};

export default InterviewDateField;

import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import {
  FieldPath,
  FieldValues,
  useController,
  UseControllerProps,
} from 'react-hook-form';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

type Props<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
> = UseControllerProps<TFieldValues, TName> & {
  control: NonNullable<UseControllerProps<TFieldValues, TName>['control']>;
  label?: string;
};

export default function InterviewDateField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>({ label = 'Interview date', ...props }: Props<TFieldValues, TName>) {
  const { field } = useController(props);
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DateTimePicker label={label} {...field} />
    </LocalizationProvider>
  );
}

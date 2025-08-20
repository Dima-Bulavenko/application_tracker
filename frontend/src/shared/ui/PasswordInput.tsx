import { Visibility, VisibilityOff } from '@mui/icons-material';
import {
  IconButton,
  InputAdornment,
  TextField,
  TextFieldProps,
} from '@mui/material';
import { useState } from 'react';
import {
  FieldValues,
  FieldPath,
  UseControllerProps,
  useController,
} from 'react-hook-form';
import { buildBaseInputProps } from 'shared/lib';

export function PasswordInput<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>(props: TextFieldProps & UseControllerProps<TFieldValues, TName>) {
  const [showPassword, setShowPassword] = useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const { field, fieldState } = useController(props);
  const baseProps = buildBaseInputProps<TFieldValues, TName>(field, fieldState);
  return (
    <TextField
      {...field}
      {...baseProps}
      {...props}
      type={showPassword ? 'text' : 'password'}
      slotProps={{
        input: {
          endAdornment: (
            <InputAdornment position='end'>
              <IconButton
                aria-label={
                  showPassword ? 'hide the password' : 'display the password'
                }
                onClick={handleClickShowPassword}
                edge='end'>
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        },
      }}
    />
  );
}

import { TextInput } from 'shared/ui';
import { type FieldComponent } from 'shared/types';
import { useController } from 'react-hook-form';
import { useState } from 'react';
import { IconButton, InputAdornment } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { zUserCreate } from 'shared/api';

const passwordHelp = zUserCreate.shape.password._def.description;

const PasswordField: FieldComponent = ({ label = 'Password', ...props }) => {
  const [showPassword, setShowPassword] = useState(false);
  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const controller = useController(props);
  return (
    <TextInput
      label={label}
      helperText={passwordHelp}
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
      {...controller}
    />
  );
};

export default PasswordField;

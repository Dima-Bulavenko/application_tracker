import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff'
import IconButton from '@mui/material/IconButton'
import InputAdornment from '@mui/material/InputAdornment'
import { useState } from 'react'
import { useController } from 'react-hook-form'
import { zUserCreate } from 'shared/api/gen/zod.gen'
import type { FieldComponent } from 'shared/types/form'
import { TextInput } from 'shared/ui/TextInput'

const passwordHelp = zUserCreate.shape.password.description

const PasswordField: FieldComponent = ({
  label = 'Password',
  helperText,
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false)
  const handleClickShowPassword = () => setShowPassword((show) => !show)
  const controller = useController(props)
  return (
    <TextInput
      label={label}
      helperText={helperText ?? passwordHelp}
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
                edge='end'
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        },
      }}
      controller={controller}
    />
  )
}

export default PasswordField

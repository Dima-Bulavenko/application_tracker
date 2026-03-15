import { Button } from 'app/components/ui/button'
import { Input } from 'app/components/ui/input'
import { Label } from 'app/components/ui/label'
import { Eye, EyeOff } from 'lucide-react'
import { useState } from 'react'
import { FieldPath, FieldValues, useController } from 'react-hook-form'
import { zUserCreate } from 'shared/api/gen/zod.gen'
import type { BaseFormFiledProps } from 'shared/types/form'

const passwordHelp = zUserCreate.shape.password.description

type PasswordFieldProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = BaseFormFiledProps<V, N> & {
  helperText?: string
}

export default function PasswordField<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ label = 'Password', helperText, ...props }: PasswordFieldProps<V, N>) {
  const [showPassword, setShowPassword] = useState(false)
  const handleClickShowPassword = () => setShowPassword((show) => !show)
  const controller = useController({ ...props })
  const { field, fieldState, formState } = controller
  const errorMessage = fieldState?.error?.message
  const id = `${field.name}_id`

  return (
    <div className='space-y-2'>
      {label && <Label htmlFor={id}>{label}</Label>}
      <div className='relative'>
        <Input
          id={id}
          type={showPassword ? 'text' : 'password'}
          disabled={
            formState.isSubmitting || formState.isLoading || field.disabled
          }
          onBlur={field.onBlur}
          onChange={(e) => {
            const val = e.target.value
            field.onChange(val.trim() === '' ? null : val)
          }}
          name={field.name}
          ref={field.ref}
          value={field.value ?? ''}
          aria-invalid={!!fieldState?.error}
          className='pr-10'
        />
        <Button
          type='button'
          variant='ghost'
          size='icon'
          className='absolute right-0 top-0 h-full px-2'
          onClick={handleClickShowPassword}
          aria-label={
            showPassword ? 'hide the password' : 'display the password'
          }
        >
          {showPassword ? (
            <EyeOff className='size-4' />
          ) : (
            <Eye className='size-4' />
          )}
        </Button>
      </div>
      {errorMessage && (
        <p className='text-sm text-destructive'>{errorMessage}</p>
      )}
      {!errorMessage && (helperText ?? passwordHelp) && (
        <p className='text-sm text-muted-foreground'>
          {helperText ?? passwordHelp}
        </p>
      )}
    </div>
  )
}

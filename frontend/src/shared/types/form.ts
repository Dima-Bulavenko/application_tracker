import type React from 'react'
import type { ReactNode } from 'react'
import type {
  Control,
  FieldPath,
  FieldValues,
  UseControllerProps,
  UseControllerReturn,
} from 'react-hook-form'

export type BaseInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<UseControllerProps<V, N>, 'control'> & {
  control: Control<V, N>
  label?: string
  helperText?: string
}

export type FieldComponent = <
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>(
  props: BaseInputProps<V, N>
) => React.JSX.Element

export type TextInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<
  React.ComponentProps<'input'>,
  'name' | 'value' | 'onChange' | 'onBlur'
> & {
  controller: UseControllerReturn<V, N>
  label?: string
  helperText?: string
}

export type TextareaInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<
  React.ComponentProps<'textarea'>,
  'name' | 'value' | 'onChange' | 'onBlur'
> & {
  controller: UseControllerReturn<V, N>
  label?: string
  helperText?: string
}

export type SelectInputProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = {
  controller: UseControllerReturn<V, N>
  options: readonly string[]
  label?: string
  helperText?: string
  humanize?: (v: string) => string
  children?: ReactNode
}

export type SelectMultipleProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = {
  controller: UseControllerReturn<V, N>
  options: readonly string[]
  label?: string
  helperText?: string
  humanize?: (v: string) => string
}

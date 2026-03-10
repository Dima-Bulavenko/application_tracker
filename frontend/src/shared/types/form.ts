import type React from 'react'
import type { ReactNode } from 'react'
import type {
  FieldPath,
  FieldValues,
  UseControllerProps,
  UseControllerReturn,
} from 'react-hook-form'

export type BaseFormFiledProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = UseControllerProps<V, N> & {
  label?: string
  description?: string
}

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

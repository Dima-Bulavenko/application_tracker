import { useDebouncedCallback } from '@tanstack/react-pacer/debouncer'
import {
  Combobox,
  ComboboxChip,
  ComboboxChips,
  ComboboxChipsInput,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
  ComboboxValue,
  useComboboxAnchor,
} from 'app/components/ui/combobox'
import { InputGroupAddon } from 'app/components/ui/input-group'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from 'app/components/ui/select'
import { Spinner } from 'app/components/ui/spinner'
import React from 'react'
import type {
  FieldPath,
  FieldValues,
  UseControllerReturn,
} from 'react-hook-form'

const defaultHumanize = (v: string) =>
  v.charAt(0).toUpperCase() + v.slice(1).replace('_', ' ')

export type SelectInputProps<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
> = {
  label?: string
  placeholder?: string
  options: readonly string[]
  controller: UseControllerReturn<TFieldValues, TName>
  id: string
}

export function SelectInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ label, options, controller, id, placeholder }: SelectInputProps<V, N>) {
  const { field, fieldState } = controller
  return (
    <Select
      name={field.name}
      onValueChange={field.onChange}
      value={field.value}
    >
      <SelectTrigger
        id={id}
        onBlur={field.onBlur}
        aria-invalid={fieldState.invalid}
        className='w-full'
      >
        {placeholder ?? <SelectValue placeholder={placeholder} />}
      </SelectTrigger>
      <SelectContent position='popper'>
        <SelectGroup>
          {label ?? <SelectLabel>{label}</SelectLabel>}
          {options.map((option) => (
            <SelectItem key={option} value={option}>
              {defaultHumanize(option)}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}

export type SelectMultipleProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<SelectInputProps<V, N>, 'label'>

export function SelectMultipleInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({ options, controller, placeholder, id }: SelectMultipleProps<V, N>) {
  const {
    field,
    fieldState,
    formState: { isSubmitting },
  } = controller
  const anchor = useComboboxAnchor()

  return (
    <Combobox
      id={id}
      name={field.name}
      multiple
      autoHighlight
      items={options}
      value={field.value}
      onValueChange={field.onChange}
      disabled={isSubmitting}
    >
      <ComboboxChips
        onBlur={field.onBlur}
        ref={anchor}
        className='w-full max-w-xs'
      >
        <ComboboxValue>
          {(values) => (
            <React.Fragment>
              {values.map((value: string) => (
                <ComboboxChip key={value}>
                  {defaultHumanize(value)}
                </ComboboxChip>
              ))}
              <ComboboxChipsInput
                aria-invalid={fieldState.invalid}
                placeholder={field.value?.length ? undefined : placeholder}
              />
            </React.Fragment>
          )}
        </ComboboxValue>
      </ComboboxChips>
      <ComboboxContent anchor={anchor}>
        <ComboboxEmpty>No items found.</ComboboxEmpty>
        <ComboboxList>
          {(item) => (
            <ComboboxItem key={item} value={item}>
              {defaultHumanize(item)}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}

type SelectSearchProps<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
> = Omit<SelectInputProps<V, N>, 'label'> & {
  isFetching: boolean
  open: boolean
  setOpen: (open: boolean) => void
}

export function AsyncSelectInput<
  V extends FieldValues = FieldValues,
  N extends FieldPath<V> = FieldPath<V>,
>({
  options,
  controller,
  placeholder,
  id,
  isFetching,
  open,
  setOpen,
}: SelectSearchProps<V, N>) {
  const {
    field,
    fieldState,
    formState: { isSubmitting },
  } = controller

  const debouncedFetching = useDebouncedCallback(field.onChange, { wait: 400 })

  return (
    <Combobox
      id={id}
      name={field.name}
      autoHighlight
      items={options}
      value={field.value}
      onValueChange={field.onChange}
      onInputValueChange={debouncedFetching}
      open={open}
      onOpenChange={setOpen}
      disabled={isSubmitting}
    >
      <ComboboxInput
        onBlur={field.onBlur}
        placeholder={placeholder}
        aria-invalid={fieldState.invalid}
      >
        {isFetching && (
          <InputGroupAddon align='inline-end'>
            <Spinner className='size-5' />
          </InputGroupAddon>
        )}
      </ComboboxInput>
      <ComboboxContent>
        {!isFetching && <ComboboxEmpty>No items found.</ComboboxEmpty>}
        <ComboboxList>
          {(item) => (
            <ComboboxItem key={item} value={item}>
              {item}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}

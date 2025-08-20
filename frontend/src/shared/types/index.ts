import {
  Control,
  FieldPath,
  FieldValues,
  UseControllerProps,
} from 'react-hook-form';
import { TextFieldProps } from '@mui/material';
import React from 'react';

export type BaseInputProps<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
> = TextFieldProps &
  UseControllerProps<TFieldValues, TName> & {
    children?: React.ReactElement;
    control: Control<TFieldValues>;
  };

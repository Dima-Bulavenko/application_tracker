import {
  Palette as lightPalette,
  ColorScheme as lightColorScheme,
} from './lightColorScheme';
import {
  Palette as darkPalette,
  ColorScheme as darkColorScheme,
} from './darkColorScheme';
import { createTheme } from '@mui/material';

export { lightPalette, lightColorScheme, darkPalette, darkColorScheme };

export const customTheme = createTheme({
  colorSchemes: {
    light: lightColorScheme,
    dark: darkColorScheme,
  },
});

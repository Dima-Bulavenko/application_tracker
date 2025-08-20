import { createContext, useContext } from 'react';

export interface ColorModeContextValue {
  mode: 'light' | 'dark';
  toggleMode: () => void;
}
export const ColorModeContext = createContext<
  ColorModeContextValue | undefined
>(undefined);
export function useColorMode() {
  const ctx = useContext(ColorModeContext);
  if (!ctx) throw new Error('ColorModeContext not provided');
  return ctx;
}

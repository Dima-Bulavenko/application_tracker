// Global theme (glass variant only)
import { createTheme, alpha, Theme } from '@mui/material/styles';

export type Mode = 'light' | 'dark';

const common = {
  shape: { borderRadius: 18 },
  typography: {
    fontFamily: `'Inter', system-ui, sans-serif`,
    h6: { fontWeight: 600 },
    button: {
      textTransform: 'none' as const,
      fontWeight: 600,
      letterSpacing: 0.2,
    },
  },
  transitions: { duration: { standard: 240 } },
};

export function buildTheme(mode: Mode): Theme {
  const isLight = mode === 'light';
  const primary = '#6366F1';
  const secondary = '#10B981';
  const bgBase = isLight ? '#F5F7FA' : '#0F1115';
  const surface = isLight ? alpha('#FFFFFF', 0.65) : alpha('#1C2128', 0.55);
  return createTheme({
    ...common,
    palette: {
      mode,
      primary: { main: primary },
      secondary: { main: secondary },
      background: { default: bgBase, paper: surface },
      divider: alpha(isLight ? '#111' : '#FFF', 0.08),
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            backdropFilter: 'blur(18px) saturate(160%)',
            backgroundImage: isLight
              ? 'linear-gradient(140deg, rgba(255,255,255,0.8), rgba(255,255,255,0.55))'
              : 'linear-gradient(140deg, rgba(28,33,40,0.9), rgba(28,33,40,0.55))',
            border: `1px solid ${alpha(isLight ? '#1E293B' : '#E2E8F0', 0.15)}`,
            transition:
              'background-color .3s, box-shadow .3s, border-color .3s',
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 14,
            backdropFilter: 'blur(10px)',
            '&.MuiButton-contained': {
              boxShadow: `0 4px 16px -4px ${alpha(primary, 0.45)}`,
            },
            '&:hover': { transform: 'translateY(-1px)' },
            transition: 'transform .2s, box-shadow .3s',
          },
        },
      },
      MuiAppBar: {
        styleOverrides: {
          root: {
            background: alpha(isLight ? '#FFFFFF' : '#0F1115', 0.55),
            backdropFilter: 'blur(20px)',
            boxShadow: `0 2px 24px -6px ${alpha(primary, 0.35)}`,
          },
        },
      },
      MuiCard: { styleOverrides: { root: { overflow: 'hidden' } } },
    },
  });
}

export const DEFAULT_THEME = 'glass';

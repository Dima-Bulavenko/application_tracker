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

// Build a theme that includes light & dark color schemes so we can rely on
// MUI v6 useColorScheme hook (supports 'system' mode automatically).
export function buildTheme(): Theme {
  const primary = '#6366F1';
  const secondary = '#10B981';
  return createTheme({
    ...common,
    cssVariables: {
      colorSchemeSelector: 'class',
    },
    colorSchemes: {
      light: {
        palette: {
          primary: { main: primary },
          secondary: { main: secondary },
          background: { default: '#F5F7FA', paper: alpha('#FFFFFF', 0.65) },
          divider: alpha('#111', 0.08),
        },
      },
      dark: {
        palette: {
          primary: { main: primary },
          secondary: { main: secondary },
          background: { default: '#0f1115ff', paper: alpha('#1C2128', 0.55) },
          divider: alpha('#FFF', 0.08),
        },
      },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: ({ theme }) => ({
            backdropFilter: 'blur(18px) saturate(160%)',
            backgroundImage:
              theme.palette.mode === 'light'
                ? 'linear-gradient(140deg, rgba(255,255,255,0.8), rgba(255,255,255,0.55))'
                : 'linear-gradient(140deg, rgba(28,33,40,0.9), rgba(28,33,40,0.55))',
            border: `1px solid ${alpha(
              theme.palette.mode === 'light' ? '#1E293B' : '#E2E8F0',
              0.15
            )}`,
            transition:
              'background-color .3s, box-shadow .3s, border-color .3s',
          }),
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
          root: ({ theme }) => ({
            background: alpha(
              theme.palette.mode === 'light' ? '#FFFFFF' : '#0F1115',
              0.55
            ),
            backdropFilter: 'blur(20px)',
            boxShadow: `0 2px 24px -6px ${alpha(primary, 0.35)}`,
          }),
        },
      },
      MuiCard: { styleOverrides: { root: { overflow: 'hidden' } } },
    },
  });
}

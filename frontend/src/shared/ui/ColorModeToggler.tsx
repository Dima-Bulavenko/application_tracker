import { useColorScheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import LightModeIcon from '@mui/icons-material/LightMode';
import NightlightRoundIcon from '@mui/icons-material/NightlightRound';
import IconButton from '@mui/material/IconButton';

type Mode = 'light' | 'dark' | 'system' | undefined;

export function ColorModeToggler() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const { mode, setMode } = useColorScheme();
  // Compute effective mode when current is 'system'

  const isDarkActive = (m: Mode) =>
    m === 'dark' || (m === 'system' && prefersDarkMode);

  const handleToggle = () => {
    if (!mode) return; // avoid hydration mismatch
    if (mode === 'system') {
      // On first visit, system is active. Toggle to the opposite of effective mode.
      setMode(prefersDarkMode ? 'light' : 'dark');
    } else {
      setMode(mode === 'light' ? 'dark' : 'light');
    }
  };

  if (!mode) return null;

  return (
    <IconButton
      aria-label='Toggle color mode'
      onClick={handleToggle}
      size='small'
      sx={{
        ml: 1,
        width: 36,
        height: 36,
        color: 'text.primary',
        '&:hover': {
          bgcolor: (theme) =>
            theme.palette.mode === 'light'
              ? theme.palette.grey[300]
              : theme.palette.grey[800],
        },
      }}>
      {isDarkActive(mode) ? (
        <NightlightRoundIcon fontSize='small' />
      ) : (
        <LightModeIcon fontSize='small' />
      )}
    </IconButton>
  );
}

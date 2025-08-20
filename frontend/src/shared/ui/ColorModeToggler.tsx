import { useColorScheme } from '@mui/material/styles';
import LightModeIcon from '@mui/icons-material/LightMode';
import SettingsBrightnessIcon from '@mui/icons-material/SettingsBrightness';
import NightlightRoundIcon from '@mui/icons-material/NightlightRound';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import React from 'react';

const modes = [
  { name: 'system', icon: <SettingsBrightnessIcon /> },
  { name: 'dark', icon: <NightlightRoundIcon /> },
  { name: 'light', icon: <LightModeIcon /> },
];

export function ColorModeToggler() {
  const { mode, setMode } = useColorScheme();
  const handleChangeMode = (event: React.MouseEvent<HTMLButtonElement>) => {
    setMode(
      (event.currentTarget?.ariaLabel as Exclude<typeof mode, undefined>) ||
        null
    );
  };

  if (!mode) return null;

  return (
    <SpeedDial
      direction='down'
      ariaLabel='Toggle color mode'
      icon={modes.find((value) => value.name === mode)?.icon}>
      {modes
        .filter((value) => value.name !== mode)
        .map((action) => (
          <SpeedDialAction
            key={action.name}
            icon={action.icon}
            slotProps={{
              tooltip: { title: action.name },
              fab: {
                onClick: handleChangeMode,
              },
            }}
          />
        ))}
    </SpeedDial>
  );
}

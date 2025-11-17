import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import type { UserRead } from 'shared/api/gen';

interface UserInfoListProps {
  user: UserRead;
}

const INFO_ITEMS = [
  { label: 'Email', getValue: (user: UserRead) => user.username },
  {
    label: 'First Name',
    getValue: (user: UserRead) => user.first_name || 'Not set',
  },
  {
    label: 'Second Name',
    getValue: (user: UserRead) => user.second_name || 'Not set',
  },
] as const;

export function UserInfoList({ user }: UserInfoListProps) {
  return (
    <List disablePadding>
      {INFO_ITEMS.map((item, index) => (
        <div key={item.label}>
          <ListItem disableGutters sx={{ py: 1.5 }}>
            <ListItemText
              primary={item.label}
              secondary={item.getValue(user)}
              slotProps={{
                primary: {
                  variant: 'body2',
                  color: 'text.secondary',
                  sx: { mb: 0.5 },
                },
                secondary: {
                  variant: 'body1',
                  color: 'text.primary',
                },
              }}
            />
          </ListItem>
          {index < INFO_ITEMS.length - 1 && <Divider />}
        </div>
      ))}
    </List>
  );
}

import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';
import { ProfileHeader } from './ProfileHeader';
import { PersonalInfoSection } from './PersonalInfoSection';
import { DangerZoneSection } from './DangerZoneSection';

export function ProfilePage() {
  return (
    <Container maxWidth='md' sx={{ py: 4 }}>
      <Stack spacing={4}>
        <ProfileHeader />
        <PersonalInfoSection />
        <DangerZoneSection />
      </Stack>
    </Container>
  );
}

import type { AppStatus } from 'shared/api/gen/types.gen';

export const statusColor: Record<
  AppStatus,
  'default' | 'primary' | 'success' | 'warning' | 'error' | 'info'
> = {
  applied: 'info',
  interview: 'warning',
  offer: 'success',
  rejected: 'error',
};

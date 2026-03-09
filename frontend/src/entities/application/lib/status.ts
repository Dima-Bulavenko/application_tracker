import type { AppStatus } from 'shared/api/gen/types.gen'

export const statusColor: Record<AppStatus, string> = {
  applied: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
  interview:
    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
  offer: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
  rejected: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
}

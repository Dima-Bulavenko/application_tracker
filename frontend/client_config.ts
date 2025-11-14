import type { CreateClientConfig } from 'shared/api/gen/client.gen';

export const createClientConfig: CreateClientConfig = (config) => ({
  ...config,
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  throwOnError: true,
});

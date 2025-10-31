import type { CreateClientConfig } from 'shared/api/gen/client.gen';

export const createClientConfig: CreateClientConfig = (config) => ({
  ...config,
  baseURL: import.meta.env.API_URL,
  withCredentials: true,
});

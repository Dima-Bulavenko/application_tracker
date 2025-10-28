import type { CreateClientConfig } from 'shared/api/gen/client.gen';

export const createClientConfig: CreateClientConfig = (config) => ({
  ...config,
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

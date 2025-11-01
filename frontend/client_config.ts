import type { CreateClientConfig } from 'shared/api/gen/client.gen';

export const createClientConfig: CreateClientConfig = (config) => ({
  ...config,
  baseURL:
    'https://fbhce6iygawzsqtorl6wefpzpi0notpv.lambda-url.eu-west-1.on.aws',
  withCredentials: true,
});

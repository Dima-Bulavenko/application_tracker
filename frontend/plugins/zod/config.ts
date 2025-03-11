import type { Plugin } from '@hey-api/openapi-ts';

import { handler } from './plugin';
import type { Config } from './types';

export const defaultConfig: Plugin.Config<Config> = {
  _dependencies: ['@hey-api/typescript'],
  _handler: handler,
  _handlerLegacy: () => {},
  myOption: true, // implements default value from types
  name: 'my-zod',
  output: 'zod',
};

/**
 * Type helper for `my-plugin` plugin, returns {@link Plugin.Config} object
 */
export const defineConfig: Plugin.DefineConfig<Config> = (config) => ({
  ...defaultConfig,
  ...config,
});

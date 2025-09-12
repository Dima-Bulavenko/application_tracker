import { defineConfig } from './plugins/zod/config';
import { defaultPlugins } from '@hey-api/openapi-ts';

export default {
  input: './openapi.json',
  output: {
    path: 'src/shared/api/gen', // nested folder so generation won't delete manual files in api root
    format: 'prettier',
  },
  plugins: [
    ...defaultPlugins,
    {
      name: '@hey-api/client-axios',
      runtimeConfigPath: './client_config.ts',
    },
    defineConfig(),
  ],
};

import { defineConfig } from './plugins/zod/config';
import { defaultPlugins } from '@hey-api/openapi-ts';

export default {
  input: './openapi.json',
  output: {
    path: 'src/client',
    format: 'prettier',
  },
  plugins: [
    ...defaultPlugins,
    {
      name: '@hey-api/client-axios',
      runtimeConfigPath: './src/client_config.ts',
    },
    defineConfig(),
  ],
};

import { defaultPlugins, defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  input: './openapi.json',
  output: {
    path: 'src/shared/api/gen',
    postProcess: ['biome:format', 'biome:lint'],
  },
  plugins: [
    ...defaultPlugins,
    {
      name: '@hey-api/client-axios',
      runtimeConfigPath: '../../../../client_config.ts',
      throwOnError: true,
    },
    {
      name: 'zod',
      responses: false,
      dates: { offset: true },
      metadata: true,
      comments: false,
    },
  ],
})

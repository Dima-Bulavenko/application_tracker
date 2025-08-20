import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
  },
  resolve: {
    alias: {
      app: fileURLToPath(new URL('./src/app', import.meta.url)),
      pages: fileURLToPath(new URL('./src/pages', import.meta.url)),
      features: fileURLToPath(new URL('./src/features', import.meta.url)),
      entities: fileURLToPath(new URL('./src/entities', import.meta.url)),
      shared: fileURLToPath(new URL('./src/shared', import.meta.url)),
      hooks: fileURLToPath(new URL('./src/hooks', import.meta.url)),
      context: fileURLToPath(new URL('./src/context', import.meta.url)),
    },
  },
});

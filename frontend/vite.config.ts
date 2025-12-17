import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
import { visualizer } from 'rollup-plugin-visualizer';
import { tanstackRouter } from '@tanstack/router-plugin/vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
      generatedRouteTree: './src/app/routeTree.gen.ts',
      routesDirectory: './src/app/routes',
    }),
    react(),
    visualizer({
      filename: 'stats.html',
      template: 'treemap',
      gzipSize: true,
      brotliSize: true,
      open: false,
    }),
  ],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api/v1': 'http://localhost:8000',
    },
  },
  resolve: {
    alias: {
      app: fileURLToPath(new URL('./src/app', import.meta.url)),
      pages: fileURLToPath(new URL('./src/pages', import.meta.url)),
      features: fileURLToPath(new URL('./src/features', import.meta.url)),
      entities: fileURLToPath(new URL('./src/entities', import.meta.url)),
      shared: fileURLToPath(new URL('./src/shared', import.meta.url)),
      widgets: fileURLToPath(new URL('./src/widgets', import.meta.url)),
    },
  },
});

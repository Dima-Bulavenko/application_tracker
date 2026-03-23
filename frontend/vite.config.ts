import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
      generatedRouteTree: './src/app/routeTree.gen.ts',
      routesDirectory: './src/app/routes',
    }),
    react({
      babel: {
        plugins: ['babel-plugin-react-compiler'],
      },
    }),
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
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          radix: [
            '@radix-ui/react-dialog',
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-select',
            '@radix-ui/react-tooltip',
          ],
          router: ['@tanstack/react-router'],
          query: ['@tanstack/react-query'],
        },
      },
    },
  },
})

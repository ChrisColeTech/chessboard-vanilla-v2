import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['localhost', 'cct-v2.ddns.net'],
    watch: {
      usePolling: true,
    },
    hmr: {
      host: 'localhost',
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
  },
})

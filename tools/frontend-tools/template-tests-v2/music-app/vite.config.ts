import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0', // Expose to all network interfaces
    allowedHosts: ['cct-v2.ddns.net'],
    hmr: {
      port: 5173,
    },
    watch: {
      usePolling: true, // Enable polling for file changes
    },
  },
  preview: {
    port: 5173,
    host: '0.0.0.0',
  }
})

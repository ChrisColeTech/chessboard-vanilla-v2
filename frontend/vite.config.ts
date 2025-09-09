import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: process.env.PORT ? parseInt(process.env.PORT) : 5173, // Use PORT env var or default to 5173
    host: true, // Allow external connections
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '.ngrok-free.app', // Allow all ngrok free domains
      '.ngrok.io', // Allow ngrok.io domains
      '.ngrok.app', // Allow ngrok.app domains
      '.trycloudflare.com' // Allow Cloudflare tunnel domains
    ],
    watch: {
      usePolling: true,
      interval: 100
    },
    hmr: {
      overlay: true
    }
  },
})

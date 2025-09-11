import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import type { ViteDevServer } from 'vite'
import type { IncomingMessage, ServerResponse } from 'http'

// Custom console plugin for Vite 7
const consolePlugin = () => {
  return {
    name: 'console-to-terminal',
    configureServer(server: ViteDevServer) {
      server.middlewares.use('/__console', (req: IncomingMessage, res: ServerResponse, next: () => void) => {
        if (req.method === 'POST') {
          let body = ''
          req.on('data', (chunk: Buffer) => {
            body += chunk.toString()
          })
          req.on('end', () => {
            try {
              const { type, args } = JSON.parse(body)
              const timestamp = new Date().toLocaleTimeString()
              console.log(`[${timestamp}] ${type.toUpperCase()}:`, ...args)
            } catch (e) {
              console.error('Failed to parse console message:', e)
            }
          })
          res.writeHead(200, { 'Content-Type': 'text/plain' })
          res.end('OK')
        } else {
          next()
        }
      })
    },
    transformIndexHtml(html: string) {
      return html.replace(
        '<head>',
        `<head>
          <script>
            (function() {
              const originalConsole = { ...console };
              ['log', 'warn', 'error', 'info'].forEach(method => {
                console[method] = function(...args) {
                  originalConsole[method](...args);
                  fetch('/__console', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: method, args: args.map(arg => 
                      typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
                    )})
                  }).catch(() => {});
                };
              });
            })();
          </script>`
      )
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), consolePlugin()],
  server: {
    port: process.env.PORT ? parseInt(process.env.PORT) : 5173,
    host: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '.ngrok-free.app',
      '.ngrok.io',
      '.ngrok.app',
      '.trycloudflare.com'
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
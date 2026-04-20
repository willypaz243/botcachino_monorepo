import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react-dom') || id.includes('react')) {
              return 'react-vendor'
            }
            if (id.includes('markdown') || id.includes('remark') || id.includes('rehype')) {
              return 'markdown-vendor'
            }
            return 'vendor'
          }
        },
      },
    },
  },
})
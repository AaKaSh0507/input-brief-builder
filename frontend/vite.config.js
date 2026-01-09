import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  const BACKEND_URL =
    env.VITE_BACKEND_URL ||
    'http://localhost:8001'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 3000,
      host: '0.0.0.0',
      strictPort: true,
    },
    define: {
      'import.meta.env.VITE_BACKEND_URL': JSON.stringify(BACKEND_URL),
    },
  }
})

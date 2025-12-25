import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
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
      'process.env.REACT_APP_BACKEND_URL': JSON.stringify(env.VITE_BACKEND_URL || env.REACT_APP_BACKEND_URL)
    }
  }
})

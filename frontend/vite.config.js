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
      allowedHosts: [
        'basic-spec-builder.preview.emergentagent.com',
        'localhost',
        '.emergentagent.com'
      ],
      hmr: {
        host: 'basic-spec-builder.preview.emergentagent.com',
        protocol: 'wss',
        clientPort: 443
      }
    },
    define: {
      'import.meta.env.VITE_BACKEND_URL': JSON.stringify(env.VITE_BACKEND_URL || env.REACT_APP_BACKEND_URL || 'https://basic-spec-builder.preview.emergentagent.com'),
      'process.env.REACT_APP_BACKEND_URL': JSON.stringify(env.VITE_BACKEND_URL || env.REACT_APP_BACKEND_URL || 'https://basic-spec-builder.preview.emergentagent.com')
    }
  }
})

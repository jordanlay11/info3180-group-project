
import { fileURLToPath, URL } from 'url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  // Load environment variables
  const env = loadEnv(mode, process.cwd(), '')
  
  // Get backend port from env, default to 8081
  const backendPort = env.VITE_BACKEND_PORT || 8081
  const targetUrl = `http://localhost:${backendPort}`
  
  console.log(`🔧 Proxying API requests to: ${targetUrl}`) 
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: targetUrl,
          changeOrigin: true,
          secure: false
        },
        '/logout': {
          target: targetUrl,
          changeOrigin: true,
          secure: false
        },
        '/auth': {
          target: targetUrl,
          changeOrigin: true,
          secure: false
        }
      }
    }
  }
})

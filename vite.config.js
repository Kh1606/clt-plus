import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// base must match the GitHub Pages subpath: https://<user>.github.io/clt-plus/
export default defineConfig({
  base: '/clt-plus/',
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
})

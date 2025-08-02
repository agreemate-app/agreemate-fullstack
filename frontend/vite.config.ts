import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: true,
    allowedHosts: [
      'agreement-generator-tunnel-tv38bryi.devinapps.com',
      'agreement-generator-tunnel-y8mkh788.devinapps.com',
      'localhost',
      '127.0.0.1'
    ]
  }
})


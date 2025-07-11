import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: ["w2fm.gridhead.net"],
    proxy: {
      "/docs": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/openapi.json": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});

import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// Port 1420 is what src-tauri/tauri.conf.json points at in development.
// In the browser (no Tauri), /rpc and /file go to the Rust dev bridge.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  clearScreen: false,
  server: { port: 1420, strictPort: true, proxy: { '/rpc': 'http://127.0.0.1:4310', '/file': 'http://127.0.0.1:4310' } },
  build: { target: 'es2022', outDir: 'dist', emptyOutDir: true },
  test: { include: ['src/**/*.test.ts'] },
});

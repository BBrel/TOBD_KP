import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/files/upload': 'http://127.0.0.1:8000',
      '/api/files/save': 'http://127.0.0.1:8000',
    },
  },
});

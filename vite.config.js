import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        background: 'src/background/background.js',
        content: 'src/content/content.js',
      },
      output: {
        entryFileNames: '[name].js',
      }
    },
    outDir: 'dist',
    emptyOutDir: true
  },
  publicDir: 'public',
  plugins: [],
});
import react from "npm:@vitejs/plugin-react";

/** @type {import('vite').UserConfig} */
export default {
  plugins: [react()],
  server: { host: true, port: 5173 },
};

import react from "@vitejs/plugin-react";
// import path from "path";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react(), tsconfigPaths()],
    // resolve: {
    //     alias: {
    //         "@": path.resolve(__dirname, "./src"),
    //     },
    // },
    server: {
        port: 3000,
        proxy: {
            "/api": {
                target: process.env.VITE_API_BASE_URL || "http://localhost:5000",
                changeOrigin: true,
            },
        },
    },
    build: {
        outDir: "dist",
        sourcemap: false,
    },
});

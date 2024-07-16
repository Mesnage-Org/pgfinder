import { purgeCss } from "vite-plugin-tailwind-purgecss";
import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import wasmPack from "vite-plugin-wasm-pack";

export default defineConfig({
  plugins: [sveltekit(), purgeCss(), wasmPack("./smithereens")],
  define: {
    WEBUI_VERSION: JSON.stringify(process.env.npm_package_version),
  },
  worker: {
    format: "es",
  },
});

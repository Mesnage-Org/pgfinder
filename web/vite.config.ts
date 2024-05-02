import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import wasmPack from 'vite-plugin-wasm-pack';

export default defineConfig({
	plugins: [sveltekit(), purgeCss(), wasmPack('./smithereens')],
	worker: {
		format: 'es'
	}
});

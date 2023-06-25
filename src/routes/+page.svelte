<script lang="ts">
	import { onMount } from 'svelte';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import MsDataUploader from './MsDataUploader.svelte';
	import MassLibraryUploader from './MassLibraryUploader.svelte';
	import AdvancedOptions from './AdvancedOptions.svelte';
	import PGFinder from '$lib/pgfinder.ts?worker';
	import fileDownload from 'js-file-download';
	// TODO:
	// 2) Add a modification selector
	// 3) Add custom mass library support
	// 4) Style and restrict formats of file upload widgets
	// 5) Add advanced options (with defaults)!
	let pgfinder: Worker | undefined;
	onMount(() => {
		pgfinder = new PGFinder();
		pgfinder.onmessage = ({ data: { type, content } }) => {
			if (type === 'Ready') {
				allowedModifications = content.allowedModifications;
				massLibraries = content.massLibraries;
				loading = false;
			} else if (type === 'Result') {
				fileDownload(content.blob, content.filename);
				processing = false;
			}
		};
	});

	let pyio: Pyio = {
		msData: [],
		massLibrary: undefined
	};

	let loading = true;
	let processing = false;
	let ready = false;

	let allowedModifications: Array<string>;
	let massLibraries: Map<string, string>;

	$: ready = !loading && !processing && pyio.msData.length !== 0 && pyio.massLibrary !== undefined;
	function runAnalysis() {
		pgfinder?.postMessage(pyio);
		processing = true;
	}
</script>

<div class="h-full flex flex-col justify-center items-center">
	<div class="card">
		<section class="flex flex-col space-y-4 justify-center p-4">
			<MsDataUploader bind:value={pyio.msData} />
			<MassLibraryUploader bind:value={pyio.massLibrary} {massLibraries} />
			<!-- Add modifications here! -->
			<AdvancedOptions />
			<button type="button" class="btn variant-filled" on:click={runAnalysis} disabled={!ready}>
				Run Analysis
			</button>
			{#if processing}
				<ProgressBar />
			{/if}
		</section>
	</div>
</div>

<script lang="ts">
	// Svelte and UI Imports
	import '../app.postcss';
	import {
		AppShell,
		Drawer,
		ProgressBar,
		storePopup,
		initializeStores
	} from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { onMount } from 'svelte';

	// Svelte Component Imports
	import AdvancedOptions from './AdvancedOptions.svelte';
	import Footer from './Footer.svelte';
	import Header from './Header.svelte';
	import LinksAndDownloads from './LinksAndDownloads.svelte';
	import MassLibraryUploader from './MassLibraryUploader.svelte';
	import MsDataUploader from './MsDataUploader.svelte';

	// Worker and JS Imports
	import PGFinder from '$lib/pgfinder.ts?worker';
	import { defaultPyio } from '$lib/constants';
	import fileDownload from 'js-file-download';

	// Initialize Stores for Drawers
	initializeStores();

	// Floating UI for Popups
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	// Pre-Declare Variables
	let pyio: Pyio = { ...defaultPyio };

	let loading = true;
	let processing = false;
	let ready = false;
	let advancedMode = false;

	let pgfinderVersion: string;
	let allowedModifications: Array<string>;
	let massLibraries: MassLibraryIndex;

	// Start PGFinder
	let pgfinder: Worker | undefined;
	onMount(() => {
		pgfinder = new PGFinder();
		pgfinder.onmessage = ({ data: { type, content } }) => {
			if (type === 'Ready') {
				pgfinderVersion = content.pgfinderVersion;
				allowedModifications = content.allowedModifications;
				massLibraries = content.massLibraries;
				loading = false;
			} else if (type === 'Result') {
				fileDownload(content.blob, content.filename);
				processing = false;
			}
		};
	});

	// Reactively compute if PGFinder is ready
	$: ready = !loading && !processing && pyio.msData !== undefined && pyio.massLibrary !== undefined;

	// Send data to PGFinder for processing
	function runAnalysis() {
		pgfinder?.postMessage(pyio);
		processing = true;
	}

	// Reactively adapt the UI when entering advanced mode
	let uiWidth: string;
	$: uiWidth = advancedMode ? 'md:w-[40rem]' : '';

	// It's nice to animate the width when opening and closing advanced mode, but
	// it seems like animating the opening leads to some jittery animations, so
	// this is just enabling the animation on close. If browsers ever put
	// transitions in their own threads, then maybe this will look nice...
	$: animateWidth = !advancedMode ? 'transition-all' : '';
</script>

<Drawer>
	<LinksAndDownloads />
</Drawer>

<AppShell>
	<svelte:fragment slot="header">
		<Header {pgfinderVersion} />
	</svelte:fragment>

	<div class="h-full flex flex-col justify-center items-center">
		<div class="card m-2 w-[20rem] {uiWidth} max-w-[90%] {animateWidth}">
			<section class="flex flex-col space-y-4 justify-center p-4">
				<MsDataUploader bind:value={pyio.msData} />
				<MassLibraryUploader bind:value={pyio.massLibrary} {massLibraries} />
				<AdvancedOptions
					bind:enabledModifications={pyio.enabledModifications}
					bind:ppmTolerance={pyio.ppmTolerance}
					bind:cleanupWindow={pyio.cleanupWindow}
					bind:consolidationPpm={pyio.consolidationPpm}
					bind:advancedMode
					{allowedModifications}
				/>
				<button type="button" class="btn variant-filled" on:click={runAnalysis} disabled={!ready}>
					Run Analysis
				</button>
				{#if processing}
					<ProgressBar />
				{/if}
			</section>
		</div>
	</div>

	<svelte:fragment slot="footer">
		<Footer />
	</svelte:fragment>
</AppShell>

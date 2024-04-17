<script lang="ts">
	// Svelte and UI Imports
	import '../app.postcss';
	import {
		AppShell,
		Drawer,
		Modal,
		ProgressBar,
		storePopup,
		initializeStores,
		getModalStore,
		type ModalSettings
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
    import FragmentsDataUploader from './FragmentsDataUploader.svelte';
    import MuropeptidesDataUploader from './MuropeptidesDataUploader.svelte';

	// Worker and JS Imports
	import PGFinder from '$lib/pgfinder.ts?worker';
	import { defaultPyio } from '$lib/constants';
    // import pg_to_fragments from '$lib/smithereens';
	import fileDownload from 'js-file-download';
	import ErrorModal from './ErrorModal.svelte';

	// Initialize Stores for Drawers and Modals
	initializeStores();

	// Get the Error Modal Store
	const modalStore = getModalStore();

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
    let fragmentsLibraries: FragmentsLibraryIndex;
    let muropeptidesLibraries: MuropeptidesLibraryIndex;

	// Start PGFinder
	let pgfinder: Worker | undefined;
	onMount(() => {
		pgfinder = new PGFinder();
		pgfinder.onmessage = ({ data: { type, content } }) => {
			if (type === 'Ready') {
				pgfinderVersion = content.pgfinderVersion;
				allowedModifications = content.allowedModifications;
				massLibraries = content.massLibraries;
                fragmentsLibraries = content.fragmentsLibraries;
                muropeptidesLibraries = content.muropeptidesLibraries;
				loading = false;
			} else if (type === 'Result') {
				fileDownload(content.blob, content.filename);
				processing = false;
			} else if (type === 'Error') {
				const modal: ModalSettings = {
					type: 'component',
					component: {
						ref: ErrorModal,
						props: {
							message: content.message
						}
					}
				};
				modalStore.trigger(modal);
				processing = false;
			}
		};
	});

	// Reactively compute if Smithereens is ready
	$: SmithereensReady = !loading && !processing && pyio.fragmentsLibrary !== undefined && pyio.muropeptidesLibrary !== undefined;

	// Send data to Smithereens for processing
	function runSmithereensAnalysis() {
    // TODO - Switch this to run smithereens WA using pyio.fragmentsLibrary and pyio.muropeptidesLibrary
		pgfinder?.postMessage(pyio);
		processing = true;
	}
	// Reactively compute if PGFinder is ready
	$: PGFinderReady = !loading && !processing && pyio.msData !== undefined && pyio.massLibrary !== undefined;

	// Send data to PGFinder for processing
	function runPGFinderAnalysis() {
		pgfinder?.postMessage(pyio);
		processing = true;
	}

	// Reactively adapt the UI when entering advanced mode
	let uiWidth: string;
	$: uiWidth = advancedMode ? 'md:w-[40rem]' : '';

	// It's nice to animate the width when opening and closing advanced mode, but
	// it seems like animating the opening leads to some jittery animations, so
	// this is just enables the animation on close. If browsers ever put
	// transitions in their own threads, then maybe this will look nice...
	$: animateWidth = !advancedMode ? 'transition-all' : '';
</script>

<Modal regionBackdrop="bg-surface-backdrop-token overflow-y-hidden" />

<Drawer>
	<LinksAndDownloads />
</Drawer>

<AppShell>
	<svelte:fragment slot="header">
		<Header {pgfinderVersion} />
	</svelte:fragment>


	<div class="h-full flex flex-cols-2 justify-center items-center">

        <!-- Smithereens -->
		<div class="card m-2 w-[20rem] {uiWidth} max-w-[90%] {animateWidth}">
			<section class="flex flex-col space-y-4 justify-center p-4">
				<FragmentsDataUploader bind:value={pyio.fragmentsLibrary} {fragmentsLibraries} />
			</section>
			<section class="flex flex-col space-y-4 justify-center p-4">
				<MuropeptidesDataUploader bind:value={pyio.muropeptidesLibrary} {muropeptidesLibraries} />
				<button type="button" class="btn variant-filled" on:click={runSmithereensAnalysis} disabled={!SmithereensReady}>
					Build database
				</button>
				{#if processing}
					<ProgressBar />
				{/if}
			</section>
		</div>

        <!-- PGFinder -->
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
				<button type="button" class="btn variant-filled" on:click={runPGFinderAnalysis} disabled={!PGFinderReady}>
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

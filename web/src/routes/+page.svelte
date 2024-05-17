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

	// PGFinder and JS Imports
	import PGFinder from '$lib/pgfinder.ts?worker';
    import Smithereens from '$lib/smithereens.ts?worker';

	import { defaultPyio, defaultSmithereens } from '$lib/constants';
	import init, { Peptidoglycan, pg_to_fragments } from 'smithereens';

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
    let smithereens: Smithereens = { ...defaultSmithereens };

	let loading = true;
    let loadingSmithereens = true;
	let processingPGFinder = false;
    let processingSmithereens = false;
	let ready = false;
	let advancedMode = false;

	let pgfinderVersion: string;
	let allowedModifications: Array<string>;
	let massLibraries: MassLibraryIndex;
    let fragmentsLibraryIndex: FragmentsLibraryIndex;
    let muropeptidesLibraryIndex: MuropeptidesLibraryIndex;
    // Need to define string reference to each of the fragmentsDataFile
    let fragmentsDataFile: string;
    let muropeptidesDataFile: string;

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
				processingPGFinder = false;
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
				processingPGFinder = false;
			}
		};
	});

    // Start Smithereens
    let smithereensWorker: Worker | undefined;
    onMount(() => {
        smithereensWorker = new Smithereens();
        smithereensWorker.onmessage = ({ data: { type, content } }) => {
            if (type === 'Ready') {
            // This is wrong I think
                fragmentsLibraryIndex = content.fragmentsLibraryIndex;
                muropeptidesLibraryIndex = content.muropeptidesLibraryIndex;
                console.log('fragmentsLibraryIndex :', fragmentsLibraryIndex);
                console.log('muropeptidesLibraryIndex :', muropeptidesLibraryIndex)
                loadingSmithereens = false;
            } else if (type === 'Process') {
                fragmentsDataFile = content.fragmentsData;
                muropeptidesDataFile = content.muropeptidesData;
                processingSmithereens = true;
            } else if (type === 'Result') {
                fileDownload(content.blob, content.filename);
	  			processingSmithereens = false;
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
				processingSmithereens = false;
          }
        };
        init().then(() => {
        	console.log("smithereens wasm loaded!");
        })
        processingSmithereens = false;
    })
	// Reactively compute if Smithereens is ready
    $: console.log(`!loadingSmithereens : `, !loadingSmithereens);
    $: console.log(`!processingSmithereens  : `, !processingSmithereens);
    $: console.log(`smithereensWorker  : `, smithereensWorker);
    $: console.log(`smithereens.fragmentsData  : `, smithereens.fragmentsData);
    $: console.log(`smithereens.muropeptidesData  : `, smithereens.muropeptidesData);
    $: console.log(`smithereens  : `, smithereens);
	$: SmithereensReady = !loadingSmithereens && !processingSmithereens && smithereens.fragmentsData !== undefined && smithereens.muropeptidesData !== undefined;
    $: console.log(`SmithereensReady : `, SmithereensReady);

	// Send data to Smithereens for processing
	function runSmithereensAnalysis() {
        console.log("We have made it into runSmithereensAnalysis!")
        // Now we call smithereens.ts
        smithereensWorker?.postMessage(smithereens)
        let pg = new Peptidoglycan("gm-AEJA")
        console.log(`Monoisotopic Mass : ${pg.monoisotopic_mass()}`);
        console.log(`Fragments :\n ${pg_to_fragments(pg)}`);
		processingSmithereens = true;
	}
	// Reactively compute if PGFinder is ready
	$: PGFinderReady = !loading && !processingPGFinder && pyio.msData !== undefined && pyio.massLibrary !== undefined;

	// Send data to PGFinder for processing
	function runPGFinderAnalysis() {
		pgfinder?.postMessage(pyio);
		processingPGFinder = true;
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
				<FragmentsDataUploader bind:value={smithereens.fragmentsData} {fragmentsLibraryIndex} />
			</section>
			<section class="flex flex-col space-y-4 justify-center p-4">
				<MuropeptidesDataUploader bind:value={smithereens.muropeptidesData} {muropeptidesLibraryIndex} />
				<button type="button" class="btn variant-filled" on:click={runSmithereensAnalysis} disabled={!SmithereensReady}>
					Build database
				</button>
				{#if processingSmithereens}
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
				{#if processingPGFinder}
					<ProgressBar />
				{/if}
			</section>
		</div>
	</div>


	<svelte:fragment slot="footer">
		<Footer />
	</svelte:fragment>
</AppShell>

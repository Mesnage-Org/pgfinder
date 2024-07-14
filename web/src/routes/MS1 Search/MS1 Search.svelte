<script lang="ts">
  import {
    ProgressBar,
    getModalStore,
    type ModalSettings,
  } from "@skeletonlabs/skeleton";
  import AdvancedOptions from "./AdvancedOptions.svelte";
  import MassDatabaseUploader from "./MassDatabaseUploader.svelte";
  import MsDataUploader from "./MsDataUploader.svelte";
  import ErrorModal from "../ErrorModal.svelte";
  import { defaultPGFinderState } from "$lib/constants";
  import PGFinder from "$lib/pgfinder.ts?worker";
  import fileDownload from "js-file-download";
  import { onMount } from "svelte";

  export let version: string;

  // Get the Error Modal Store
  const modalStore = getModalStore();

  // Declare component state
  let state: PGFinderState = { ...defaultPGFinderState };
  let allowedModifications: Array<string>;
  let massLibraries: MassLibraryIndex;
  let loading = true;
  let processing = false;
  let advancedMode = false;

  // Start PGFinder and attach callbacks
  let pgfinder: Worker;
  onMount(() => {
    pgfinder = new PGFinder();
    pgfinder.onmessage = ({ data: msg }) => {
      switch (msg.type) {
        case "Ready":
          version = msg.version;
          allowedModifications = msg.allowedModifications;
          massLibraries = msg.massLibraries;
          loading = false;
          break;
        case "Result":
          fileDownload(msg.blob, msg.filename);
          processing = false;
          break;
        case "Error":
          const modal: ModalSettings = {
            type: "component",
            component: {
              ref: ErrorModal,
              props: {
                message: msg.message,
              },
            },
          };
          modalStore.trigger(modal);
          processing = false;
          break;
      }
    };
  });

  // Send data to PGFinder for processing
  function runAnalysis() {
    pgfinder.postMessage(state);
    processing = true;
  }

  // Reactively compute if PGFinder is ready
  $: ready =
    !loading &&
    !processing &&
    state.msData !== undefined &&
    state.massLibrary !== undefined;

  // Reactively adapt the UI when entering advanced mode
  $: uiWidth = advancedMode ? "md:w-[40rem]" : "";

  // It's nice to animate the width when opening and closing advanced mode, but
  // it seems like animating the opening leads to some jittery animations, so
  // this is just enables the animation on close. If browsers ever put
  // transitions in their own threads, then maybe this will look nice...
  $: animateWidth = !advancedMode ? "transition-all" : "";
</script>

<div
  class="card m-2 w-[20rem] {uiWidth} max-w-[90%] {animateWidth}"
  data-testid="MS1 Search"
>
  <section class="flex flex-col space-y-4 justify-center p-4">
    <MsDataUploader bind:value={state.msData} />

    <MassDatabaseUploader bind:value={state.massLibrary} {massLibraries} />

    <AdvancedOptions
      bind:enabledModifications={state.enabledModifications}
      bind:ppmTolerance={state.ppmTolerance}
      bind:cleanupWindow={state.cleanupWindow}
      bind:consolidationPpm={state.consolidationPpm}
      bind:advancedMode
      {allowedModifications}
    />

    <button
      type="button"
      class="btn variant-filled"
      on:click={runAnalysis}
      disabled={!ready}
    >
      Run Analysis
    </button>

    {#if processing}
      <ProgressBar />
    {/if}
  </section>
</div>

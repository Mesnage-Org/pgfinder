<script lang="ts">
  // Pre-Declare Variables
  let smithereens: SmithereensState = { ...defaultSmithereens };

  let loadingSmithereens = true;
  let processingSmithereens = false;

  // Start Smithereens
  let smithereensWorker: Worker | undefined;
  onMount(() => {
    smithereensWorker = new Smithereens();
    smithereensWorker.onmessage = ({ data: { type, content } }) => {
      if (type === "Ready") {
        loadingSmithereens = false;
      } else if (type === "Process") {
        processingSmithereens = true;
      } else if (type === "Result") {
        fileDownload(content.blob, content.filename);
        processingSmithereens = false;
      } else if (type === "Error") {
        const modal: ModalSettings = {
          type: "component",
          component: {
            ref: ErrorModal,
            props: {
              message: content.message,
            },
          },
        };
        modalStore.trigger(modal);
        processingSmithereens = false;
      }
    };
    processingSmithereens = false;
  });
  // Reactively compute if Smithereens is ready
  $: SmithereensReady =
    !loadingSmithereens &&
    !processingSmithereens &&
    smithereens.muropeptidesData !== undefined;
  $: console.log(`SmithereensReady : `, SmithereensReady);

  // Send data to Smithereens for processing
  function runSmithereensAnalysis() {
    // Now we call smithereens.ts
    smithereensWorker?.postMessage(smithereens);
    processingSmithereens = true;
  }
</script>

<div class="card m-2 w-[20rem] max-w-[90%]" data-testid="Smithereens">
  <section class="flex flex-col space-y-4 justify-center p-4">
    <MuropeptidesDataUploader
      bind:value={smithereens.muropeptidesData}
      {muropeptidesLibraryIndex}
    />
    <button
      type="button"
      class="btn variant-filled"
      on:click={runSmithereensAnalysis}
      disabled={!SmithereensReady}
    >
      Build database
    </button>
    {#if processingSmithereens}
      <ProgressBar />
    {/if}
  </section>
</div>

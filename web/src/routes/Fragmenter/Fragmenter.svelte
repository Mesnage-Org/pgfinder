<script lang="ts">
  import {
    ProgressBar,
    Tab,
    TabGroup,
    getModalStore,
    type ModalSettings,
  } from "@skeletonlabs/skeleton";
  import ErrorModal from "../ErrorModal.svelte";
  import { onMount } from "svelte";
  import Smithereens from "$lib/smithereens.ts?worker";
  import fileDownload from "js-file-download";
  import Single from "./Single.svelte";

  // Get the Error Modal Store
  const modalStore = getModalStore();

  let loading = true;
  let processing = false;
  let bulk = true;

  // Single Structure State
  let validStructure = true;
  let structure = "";

  $: structure, runValidate();

  function runValidate() {
    let msg: SmithereensReq = {
      type: "ValidateReq",
      structure,
    };
    smithereens?.postMessage(msg);
  }

  // Start Smithereens
  let smithereens: Worker;
  onMount(() => {
    smithereens = new Smithereens();
    smithereens.onmessage = ({ data: msg }: MessageEvent<SmithereensRes>) => {
      switch (msg.type) {
        case "Ready":
          loading = false;
          break;
        case "ValidateRes":
          validStructure = true;
          break;
        case "FragmentRes":
          fileDownload(msg.blob, msg.filename);
          processing = false;
          break;
        case "SingleErr":
          validStructure = false;
          break;
      }
      processing = false;
    };
  });
  // Reactively compute if Smithereens is ready
  $: ready = !loading && !processing && !bulk && structure && validStructure;

  function fragment() {
    if (bulk) {
      console.error("TODO");
    } else {
      let msg: SmithereensReq = {
        type: "FragmentReq",
        structure,
      };
      smithereens.postMessage(msg);
    }
    processing = true;
  }

  // Reactively compute the name of the fragment button
  $: plural = bulk ? "s" : "";
</script>

<div class="card m-2 w-[20rem] max-w-[90%]" data-testid="Fragmenter">
  <section class="flex flex-col items-center p-4">
    <h5 class="pb-1 h5">Fragment Generator</h5>
    <TabGroup class="w-full" justify="justify-center">
      <Tab bind:group={bulk} name="bulk" value={true}>Bulk</Tab>
      <Tab bind:group={bulk} name="single" value={false}>Single</Tab>
      <svelte:fragment slot="panel">
        {#if bulk}
          <!-- FIXME: Don't forget to add the space-y-4 to the inner div here... -->
          <p>TODO</p>
          {#if processing}
            <ProgressBar />
          {/if}
        {:else}
          <Single bind:structure {validStructure} />
        {/if}
      </svelte:fragment>
    </TabGroup>

    <button
      type="button"
      class="btn variant-filled w-full mt-4"
      on:click={fragment}
      disabled={!ready}
    >
      Fragment Structure{plural}
    </button>
    {#if processing}
      <ProgressBar class="mt-4" />
    {/if}
  </section>
</div>

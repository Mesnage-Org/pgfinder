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

  let loadingSmithereens = true;
  let processingSmithereens = false;
  let bulk = true;

  // Single Structure State
  let validStructure = true;
  let structure = "";

  $: structure, runValidate();

  function runValidate() {
    let msg: SmithereensReq = {
      type: "ValidateReq",
      structure
    }
    smithereens?.postMessage(msg);
  }

  // Start Smithereens
  let smithereens: Worker;
  onMount(() => {
    smithereens = new Smithereens();
    smithereens.onmessage = ({ data: msg }: MessageEvent<SmithereensRes>) => {
      console.log(msg);
      switch (msg.type) {
        case "Ready":
          loadingSmithereens = false;
          break;
        case "ValidateRes":
          validStructure = true;
          break;
        case "FragmentRes":
          fileDownload(msg.blob, msg.filename);
          processingSmithereens = false
          break;
        case "SingleErr":
          validStructure = false;
          break;
      }
    //   if (type === "Ready") {
    //     loadingSmithereens = false;
    //   } else if (type === "Process") {
    //     processingSmithereens = true;
    //   } else if (type === "Result") {
    //     fileDownload(content.blob, content.filename);
    //     processingSmithereens = false;
    //   } else if (type === "Error") {
    //     const modal: ModalSettings = {
    //       type: "component",
    //       component: {
    //         ref: ErrorModal,
    //         props: {
    //           message: content.message,
    //         },
    //       },
    //     };
    //     modalStore.trigger(modal);
    //     processingSmithereens = false;
    //   }
    // };
    processingSmithereens = false;
  }});
  // Reactively compute if Smithereens is ready
  $: ready =
    !loadingSmithereens &&
    !processingSmithereens &&
    (!bulk && structure && validStructure);

  function fragment() {
    if (bulk) {
      console.error("TODO");
    } else {
      let msg: SmithereensReq = {
        type: "FragmentReq",
        structure
      };
      smithereens.postMessage(msg);
    }
    processingSmithereens = true;
  }

  // Reactively compute the name of the fragment button
  $: plural = bulk ? "s" : "";
</script>

<div class="card m-2 w-[20rem] max-w-[90%]" data-testid="Fragmenter">
  <section class="flex flex-col space-y-4 items-center p-4">
    <h5 class="pb-1 h5">Fragment Generator</h5>
    <TabGroup class="w-full" justify="justify-center">
      <Tab bind:group={bulk} name="bulk" value={true}>Bulk</Tab>
      <Tab bind:group={bulk} name="single" value={false}>Single</Tab>
      <svelte:fragment slot="panel">
        {#if bulk}
          <p>TODO</p>
          {#if processingSmithereens}
            <ProgressBar />
          {/if}
        {:else}
          <Single bind:structure {validStructure} />
        {/if}
      </svelte:fragment>
    </TabGroup>

    <button
      type="button"
      class="btn variant-filled w-full"
      on:click={fragment}
      disabled={!ready}
    >
      Fragment Structure{plural}
    </button>
    {#if processingSmithereens}
      <ProgressBar />
    {/if}
  </section>
</div>

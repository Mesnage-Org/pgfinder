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
  let tab = "bulk";

  // Single Structure State
  let validStructure = true;
  let structure = "";
  let mass = "";

  $: structure, runSingle();

  function runSingle() {
    let msg: SmithereensReq = {
      type: "MassReq",
      structure,
    };
    smithereens?.postMessage(msg);
  }

  // Start Smithereens
  let smithereens: Worker;
  onMount(() => {
    smithereens = new Smithereens();
    smithereens.onmessage = ({ data: msg }) => {
      switch (msg.type) {
        case "Ready":
          loadingSmithereens = false;
          break;
        case "MassRes":
          validStructure = true;
          mass = msg.mass;
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
    };
  });
  // Reactively compute if Smithereens is ready
  $: SmithereensReady =
    !loadingSmithereens &&
    !processingSmithereens;
</script>

<div class="card m-2 w-[20rem] max-w-[90%]" data-testid="Mass Calculator">
  <section class="flex flex-col space-y-4 items-center p-4">
    <h5 class="pb-1 h5">Mass Calculator</h5>
    <TabGroup class="w-full" justify="justify-center">
      <Tab bind:group={tab} name="built-in" value={"bulk"}>Bulk</Tab>
      <Tab bind:group={tab} name="custom" value={"single"}>Single</Tab>
      <svelte:fragment slot="panel">
        {#if tab === "bulk"}
          <p>TODO</p>
          <button
            type="button"
            class="btn variant-filled"
            on:click={() => console.log("Hot stuff!")}
            disabled={!SmithereensReady}
          >
            Build database
          </button>
          {#if processingSmithereens}
            <ProgressBar />
          {/if}
        {:else if tab === "single"}
          <Single bind:structure {validStructure} {mass} />
        {/if}
      </svelte:fragment>
    </TabGroup>
  </section>
</div>

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
  import Bulk from "./Bulk.svelte";

  export let version: string | undefined;

  // Get the Error Modal Store
  const modalStore = getModalStore();

  let loading = true;
  let processing = false;
  let tab = "bulk";

  // Bulk Database State
  let structures: File | undefined;

  function runBulk() {
    let msg: SMassesReq = {
      type: "MassesReq",
      // SAFETY: Button only enabled if `structures` has been set
      structures: structures as File,
    };
    smithereens.postMessage(msg);
    processing = true;
  }

  // Single Structure State
  let validStructure = true;
  let structure = "";
  let mass = "";

  $: structure, runSingle();

  function runSingle() {
    let msg: SMassReq = {
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
          version = msg.version;
          loading = false;
          break;
        case "MassRes":
          validStructure = true;
          mass = msg.mass;
          break;
        case "MassesRes":
          fileDownload(msg.blob, msg.filename);
          processing = false;
          break;
        case "SingleErr":
          validStructure = false;
          break;
        case "BulkErr":
          const message =
            `The structure '${msg.structure}' on line ${msg.line} was invalid` +
            ". Please replace it with a valid structure and try again.";
          const modal: ModalSettings = {
            type: "component",
            component: {
              ref: ErrorModal,
              props: {
                message,
                manualError: true,
              },
            },
          };
          modalStore.trigger(modal);
          break;
      }
      processing = false;
    };
  });
  // Reactively compute if Smithereens is ready
  $: ready = !loading && !processing && structures !== undefined;
</script>

<div class="card m-2 w-[20rem] max-w-[90%]" data-testid="Mass Calculator">
  <section class="flex flex-col items-center p-4">
    <h5 class="pb-1 h5">Mass Calculator</h5>
    <TabGroup class="w-full" justify="justify-center">
      <Tab bind:group={tab} name="built-in" value={"bulk"}>Bulk</Tab>
      <Tab bind:group={tab} name="custom" value={"single"}>Single</Tab>
      <svelte:fragment slot="panel">
        {#if tab === "bulk"}
          <Bulk bind:structures buildCommand={runBulk} {ready} />
        {:else if tab === "single"}
          <Single bind:structure {validStructure} {mass} />
        {/if}
      </svelte:fragment>
    </TabGroup>
    {#if processing}
      <ProgressBar class="mt-4" />
    {/if}
  </section>
</div>

<script lang="ts">
  import { run } from "svelte/legacy";

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

  interface Props {
    version: string | undefined;
  }

  let { version = $bindable() }: Props = $props();

  // Get the Error Modal Store
  const modalStore = getModalStore();

  let loading = $state(true);
  let processing = $state(false);
  let tab = $state("bulk");

  // Bulk Database State
  let structures: File | undefined = $state();

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
  let validStructure = $state(true);
  let structure = $state("");
  let mass = $state("");
  let smiles = $state("");

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
          smiles = msg.smiles;
          break;
        case "MassesRes":
          fileDownload(msg.blob, msg.filename);
          processing = false;
          break;
        case "SingleErr":
          validStructure = false;
          break;
        case "BulkErr": {
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
      }
      processing = false;
    };
  });
  // TODO: Once we move to Svelte 5, there will be a better way to do this that
  // doesn't trigger this lint!
  // eslint-disable-next-line @typescript-eslint/no-unused-expressions
  run(() => {
    structure, runSingle();
  });
  // Reactively compute if Smithereens is ready
  let ready = $derived(!loading && !processing && structures !== undefined);
</script>

<div class="flex flex-col items-center">
  <h3 class="pb-1 h3">Mass Calculator</h3>
  <div class="card m-2 w-[20rem] max-w-[90%]" data-testid="Mass Calculator">
    <section class="flex flex-col items-center p-4">
      <TabGroup class="w-full" justify="justify-center">
        <Tab bind:group={tab} name="built-in" value={"bulk"}>Bulk</Tab>
        <Tab bind:group={tab} name="custom" value={"single"}>Single</Tab>
        {#snippet panel()}
          {#if tab === "bulk"}
            <Bulk bind:structures buildCommand={runBulk} {ready} />
          {:else if tab === "single"}
            <Single bind:structure {validStructure} {mass} {smiles} />
          {/if}
        {/snippet}
      </TabGroup>
      {#if processing}
        <ProgressBar class="mt-4" />
      {/if}
    </section>
  </div>
</div>

<script lang="ts">
  import {
    FileDropzone,
    ProgressRadial,
    AccordionItem,
    Accordion,
  } from "@skeletonlabs/skeleton";
  import { base } from "$app/paths";
  import { onMount } from "svelte";
  import Tooltip from "../Tooltip.svelte";

  export let structures: File | undefined;
  export let buildCommand: () => void;
  export let ready: boolean;

  let files: FileList;
  let structuresIndex: StructuresIndex | undefined;

  onMount(async () => {
    const res = await fetch(`${base}/data/structures_templates/index.json`);
    structuresIndex = JSON.parse(await res.text());
  });

  function structuresUploaded() {
    const file = files.item(0);
    if (file) {
      structures = file;
    }
  }
</script>

<div class="flex flex-col items-center space-y-4">
  <FileDropzone
    name="structure-list"
    bind:files
    on:change={structuresUploaded}
    accept=".txt"
  >
    <svelte:fragment slot="message">
      {#if structures === undefined}
        <p><b>Upload a file</b> or drag and drop</p>
      {:else}
        <p>{structures.name}</p>
      {/if}
    </svelte:fragment>
    <svelte:fragment slot="meta">
      {#if !structures}
        Muropeptide Structures (.txt)
      {/if}
    </svelte:fragment>
  </FileDropzone>
  <Accordion class="w-full">
    <AccordionItem>
      <svelte:fragment slot="summary">Template Lists</svelte:fragment>
      <svelte:fragment slot="content">
        {#if structuresIndex}
          {#each Object.entries(structuresIndex) as [species, info]}
            <a href="{base}/data/structures_templates/{info['file']}" download>
              <div
                class="flex items-center py-2 px-4 hover:variant-soft-surface"
              >
                <p class="grow"><i>{species}</i></p>
                {#if info["citation"]}
                  <Tooltip type="info" width="w-44">
                    {info["citation"]}
                  </Tooltip>
                {/if}
              </div>
            </a>
          {/each}
        {:else}
          <div class="flex justify-center">
            <ProgressRadial />
          </div>
        {/if}
      </svelte:fragment>
    </AccordionItem>
  </Accordion>
  <button
    type="button"
    class="btn variant-filled w-full"
    on:click={buildCommand}
    disabled={!ready}
  >
    Build Database
  </button>
</div>

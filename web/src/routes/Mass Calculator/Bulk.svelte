<script lang="ts">
  import {
    Accordion, FileUpload, ProgressRing } from "@skeletonlabs/skeleton-svelte";
  import { base } from "$app/paths";
  import { onMount } from "svelte";
  import Tooltip from "../Tooltip.svelte";

  interface Props {
    structures: File | undefined;
    buildCommand: () => void;
    ready: boolean;
  }

  let { structures = $bindable(), buildCommand, ready }: Props = $props();

  let files: FileList = $state();
  let structuresIndex: StructuresIndex | undefined = $state();

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
  <FileUpload
    name="structure-list"
    bind:files
    on:change={structuresUploaded}
    accept=".txt"
  >
    {#snippet message()}
      {#if structures === undefined}
        <p><b>Upload a file</b> or drag and drop</p>
      {:else}
        <p>{structures.name}</p>
      {/if}
    {/snippet}
    {#snippet meta()}
      {#if !structures}
        Muropeptide Structures (.txt)
      {/if}
    {/snippet}
  </FileUpload>
  <Accordion class="w-full">
    <Accordion.Item>
      {#snippet summary()}
        Template Lists
      {/snippet}
      {#snippet content()}
        {#if structuresIndex}
          {#each Object.entries(structuresIndex) as [species, info]}
            <a href="{base}/data/structures_templates/{info['file']}" download>
              <div
                class="flex items-center py-2 px-4 hover:preset-tonal-surface"
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
            <ProgressRing />
          </div>
        {/if}
      {/snippet}
    </Accordion.Item>
  </Accordion>
  <button
    type="button"
    class="btn preset-filled w-full"
    onclick={buildCommand}
    disabled={!ready}
  >
    Build Database
  </button>
</div>

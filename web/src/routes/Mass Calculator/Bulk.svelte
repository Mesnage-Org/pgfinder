<script lang="ts">
  import {
    FileDropzone,
    TabGroup,
    Tab,
    ProgressRadial,
  } from "@skeletonlabs/skeleton";
  import Tooltip from "../Tooltip.svelte";
  import { onMount } from "svelte";

  export let structures: File | undefined;
  export let buildCommand: () => void;
  export let ready: boolean;

  let files: FileList;
  let structuresIndex: StructuresIndex | undefined;

  onMount(async () => {
    const res = await fetch("/data/structures_templates/index.json");
    structuresIndex = JSON.parse(await res.text());
  });

  function structuresUploaded() {
    const file = files.item(0);
    if (file) {
      structures = file;
    }
  }
</script>

<!--
{#each Object.entries(muropeptidesLibraryIndex) as [speciesMuropeptides, librariesMuropeptides], speciesIdMuropeptides}
  <label>
    <div class="flex items-center">
      <input
        type="radio"
        name="muropeptides-library"
        bind:group={value}
        value={{ name: librariesMuropeptides["File"], content: null }}
      />
      <p class="grow"><i>{speciesMuropeptides}</i></p>
      <Tooltip popupId="library{speciesIdMuropeptides}">
        {librariesMuropeptides["Description"]}
      </Tooltip>
    </div>
  </label>
{/each}
-->
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
  {#if structuresIndex}{:else}
    <div class="flex justify-center">
      <ProgressRadial />
    </div>
  {/if}
  <button
    type="button"
    class="btn variant-filled w-full"
    on:click={buildCommand}
    disabled={!ready}
  >
    Build Database
  </button>
</div>

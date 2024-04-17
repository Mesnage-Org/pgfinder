<script lang="ts">
	import { Accordion, AccordionItem, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import Tooltip from './Tooltip.svelte';
	export let value: VirtFile | undefined;
	export let muropeptidesLibraries: MuropeptidesLibraryIndex;
</script>

{#each Object.entries(muropeptidesLibraries) as [speciesMuropeptides, librariesMuropeptides], speciesIdMuropeptides}
    <label>
      <div class="flex items-center">
        <input
          type="radio"
          name="muropeptides-library"
          bind:group={value}
          value={{ name: librariesMuropeptides['File'], content: null }}
        />
<!--        <p class="grow"><i>{speciesMuropeptides}</i> (<code>{librariesMuropeptides['File']}</code>)</p> -->
        <p class="grow"><i>{speciesMuropeptides}</i></p>
        <Tooltip popupId="library{speciesIdMuropeptides}">
          {librariesMuropeptides['Description']}
        </Tooltip>
      </div>
    </label>
{/each}

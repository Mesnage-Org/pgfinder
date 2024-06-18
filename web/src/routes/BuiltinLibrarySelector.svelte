<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    ListBox,
    ListBoxItem,
  } from "@skeletonlabs/skeleton";
  import Tooltip from "./Tooltip.svelte";
  export let value: VirtFile | undefined;
  export let massLibraries: MassLibraryIndex;
</script>

<Accordion autocollapse class="w-full">
  {#each Object.entries(massLibraries) as [species, libraries], speciesId}
    <AccordionItem>
      <svelte:fragment slot="summary"><i>{species}</i></svelte:fragment>
      <svelte:fragment slot="content">
        <ListBox>
          {#each Object.entries(libraries) as [name, library], libraryId}
            <ListBoxItem
              bind:group={value}
              name="mass-library"
              value={{ name: library["File"], content: null }}
            >
              <div class="flex items-center">
                <p class="grow">{name}</p>
                <Tooltip popupId="library{speciesId}{libraryId}">
                  {library["Description"]}
                </Tooltip>
              </div>
            </ListBoxItem>
          {/each}
        </ListBox>
      </svelte:fragment>
    </AccordionItem>
  {/each}
</Accordion>

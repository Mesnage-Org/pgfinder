<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    ListBox,
    ListBoxItem,
  } from "@skeletonlabs/skeleton";
  import Tooltip from "../Tooltip.svelte";
  interface Props {
    value: VirtFile | undefined;
    massLibraries: MassLibraryIndex;
  }

  let { value = $bindable(), massLibraries }: Props = $props();
</script>

<Accordion autocollapse class="w-full">
  {#each Object.entries(massLibraries) as [species, libraries]}
    <AccordionItem>
      {#snippet summary()}
        <i>{species}</i>
      {/snippet}
      {#snippet content()}
        <ListBox>
          {#each Object.entries(libraries) as [name, library]}
            <ListBoxItem
              bind:group={value}
              name="mass-library"
              value={{ name: library["file"], content: null }}
            >
              <div class="flex items-center">
                <p class="grow">{name}</p>
                <Tooltip type="info">
                  {library["description"]}
                </Tooltip>
              </div>
            </ListBoxItem>
          {/each}
        </ListBox>
      {/snippet}
    </AccordionItem>
  {/each}
</Accordion>

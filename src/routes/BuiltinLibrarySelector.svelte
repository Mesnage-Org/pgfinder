<script lang="ts">
	import { Accordion, AccordionItem, ListBox, ListBoxItem, popup } from '@skeletonlabs/skeleton';
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
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
							value={{ name: library['File'], content: null }}
						>
							<div class="flex items-center">
								<p class="grow">{name}</p>
								<div
									class="[&>*]:pointer-events-none"
									use:popup={{
										event: 'hover',
										target: `library${speciesId}${libraryId}`,
										placement: 'top'
									}}
								>
									<Fa icon={faCircleInfo} />
								</div>
							</div>
							<div
								class="card p-4 variant-filled-secondary max-w-md"
								data-popup="library{speciesId}{libraryId}"
							>
								<p class="text-center">{library['Description']}</p>
								<div class="arrow variant-filled-secondary" />
							</div>
						</ListBoxItem>
					{/each}
				</ListBox>
			</svelte:fragment>
		</AccordionItem>
	{/each}
</Accordion>

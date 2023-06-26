<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import ModificationSelector from './ModificationSelector.svelte';
	export let enabledModifications: Array<string>;
	export let allowedModifications: Array<string> | undefined;
	export let ppmTolerance: number;
	export let cleanupWindow: number;
</script>

<Accordion class="w-full">
	<AccordionItem>
		<svelte:fragment slot="summary">Advanced Options</svelte:fragment>
		<svelte:fragment slot="content">
			<ModificationSelector bind:value={enabledModifications} {allowedModifications} />
			<div class="flex flex-col items-center">
				<h5 class="pb-1 h5">PPM Tolerance</h5>
				<input bind:value={ppmTolerance} class="input" type="number" step="1" min="0" />
			</div>
			<div class="flex flex-col items-center">
				<h5 class="pb-1 h5">Cleanup Window</h5>
				<input bind:value={cleanupWindow} class="input" type="number" step="0.1" min="0" />
			</div>
		</svelte:fragment>
	</AccordionItem>
</Accordion>

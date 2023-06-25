<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import ModificationSelector from './ModificationSelector.svelte';
	export let enabledModifications: Array<string>;
	export let allowedModifications: Array<string> | undefined;
</script>

<Accordion class="w-full">
	<AccordionItem>
		<svelte:fragment slot="summary">Advanced Options</svelte:fragment>
		<svelte:fragment slot="content">
			<ModificationSelector bind:value={enabledModifications} {allowedModifications} />
		</svelte:fragment>
	</AccordionItem>
</Accordion>

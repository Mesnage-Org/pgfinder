<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
</script>

<Accordion class="pb-4 px-4">
	<AccordionItem>
		<svelte:fragment slot="summary">Advanced Options</svelte:fragment>
		<svelte:fragment slot="content">
			<p>Certainly some things!</p>
		</svelte:fragment>
	</AccordionItem>
</Accordion>

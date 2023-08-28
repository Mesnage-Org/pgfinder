<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faBars } from '@fortawesome/free-solid-svg-icons';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
			<svelte:fragment slot="lead">
				<Fa icon={faBars} size="lg" />
			</svelte:fragment>
			<strong class="text-xl">PGFinder</strong>
			<svelte:fragment slot="trail">
				<a
					class="btn btn-sm variant-ghost-surface"
					href="https://github.com/Mesnage-Org/pgfinder"
					target="_blank"
					rel="noreferrer"
				>
					GitHub
				</a>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>

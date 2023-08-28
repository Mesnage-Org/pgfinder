<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar, Drawer } from '@skeletonlabs/skeleton';
	import LinksAndDownloads from './LinksAndDownloads.svelte';
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faBars } from '@fortawesome/free-solid-svg-icons';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	// Initialize Stores for Drawers
	import { initializeStores, getDrawerStore } from '@skeletonlabs/skeleton';
	initializeStores();
	const drawerStore = getDrawerStore();

	function openDrawer(): void {
		drawerStore.open({
			width: 'w-96'
		});
	}
</script>

<!-- Drawer for Links and Downloads -->
<Drawer>
	<LinksAndDownloads />
</Drawer>
<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
			<svelte:fragment slot="lead">
				<button on:click={openDrawer}>
					<Fa icon={faBars} size="lg" />
				</button>
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
	<svelte:fragment slot="footer">
		<!-- Footer -->
		<AppBar gridColumns="grid-cols-1" slotDefault="place-self-center">
			<p class="text-center text-sm">
				Any issues or suggestions? Please get in touch!
				<br />
				<a href="mailto:smesnage@sheffield.ac.uk">
					<strong>smesnage@sheffield.ac.uk</strong>
				</a>
			</p>
		</AppBar>
	</svelte:fragment>
</AppShell>

<script lang="ts">
	import { AppBar } from '@skeletonlabs/skeleton';
	import Fa from 'svelte-fa';
	import { faBars, faBook } from '@fortawesome/free-solid-svg-icons';
	import { faGithub } from '@fortawesome/free-brands-svg-icons';
	import { getDrawerStore } from '@skeletonlabs/skeleton';
	export let pgfinderVersion: string | undefined;

	const drawerStore = getDrawerStore();
	function openDrawer(): void {
		drawerStore.open({
			width: 'max-w-[80%] w-96'
		});
	}
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">
		<button on:click={openDrawer}>
			<Fa icon={faBars} size="lg" />
		</button>
	</svelte:fragment>

	<p class="text-xl text-center">
		<strong>
			PGFinder
			{#if pgfinderVersion}
				(v{pgfinderVersion})
			{/if}
		</strong>
	</p>

	<svelte:fragment slot="trail">
		<a href="https://pgfinder.readthedocs.io/en/latest/usage.html" target="_blank">
			<Fa icon={faBook} size="lg" />
		</a>

		<a href="https://github.com/Mesnage-Org/pgfinder" target="_blank">
			<Fa icon={faGithub} size="lg" />
		</a>
	</svelte:fragment>
</AppBar>

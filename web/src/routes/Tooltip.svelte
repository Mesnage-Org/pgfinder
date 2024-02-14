<script lang="ts">
	import { popup, type PopupSettings } from '@skeletonlabs/skeleton';
	import Fa from 'svelte-fa';
	import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
	export let popupId: string;
	export let style: string = '';

	let tooltip: PopupSettings = {
		event: 'hover',
		target: popupId,
		placement: 'top'
	};
</script>

<div class="{style} [&>*]:pointer-events-none" use:popup={tooltip}>
	<Fa icon={faCircleInfo} class="inline" />
</div>
<div
	class="card p-4 variant-filled-secondary w-96 max-w-[calc(100vw-16px)] z-50"
	data-popup={popupId}
>
	<p class="text-center font-normal font-token">
		<slot />
	</p>
	<div class="arrow variant-filled-secondary" />
</div>

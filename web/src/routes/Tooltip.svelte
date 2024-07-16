<script lang="ts">
  import { popup, type PopupSettings } from "@skeletonlabs/skeleton";
  import Fa from "svelte-fa";
  import {
    faCircleInfo,
    faTriangleExclamation,
    type IconDefinition,
  } from "@fortawesome/free-solid-svg-icons";
  import { onMount } from "svelte";

  export let type: string;
  export let style: string = "";
  export let width: string = "w-96";

  let popupId: `${string}-${string}-${string}-${string}-${string}`;
  let tooltip: PopupSettings;

  onMount(() => {
    popupId = window.crypto.randomUUID();
    tooltip = {
      event: "hover",
      target: popupId,
      placement: "top",
    };
  });

  let icon: IconDefinition;
  let color: string;

  switch (type) {
    case "info":
      icon = faCircleInfo;
      color = "variant-filled-secondary";
      break;
    case "warn":
      icon = faTriangleExclamation;
      color = "variant-filled-error";
      break;
  }
</script>

{#if tooltip}
  <div class="{style} [&>*]:pointer-events-none" use:popup={tooltip}>
    <Fa {icon} class="inline" />
  </div>
  <div
    class="card p-4 {color} {width} max-w-[calc(100vw-16px)] z-50"
    data-popup={popupId}
  >
    <p class="text-center font-normal font-token">
      <slot />
    </p>
    <div class="arrow {color}" />
  </div>
{/if}

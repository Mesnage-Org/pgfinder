<script lang="ts">
  import { AppBar } from "@skeletonlabs/skeleton-svelte";
  import Fa from "svelte-fa";
  import { faBars, faBook } from "@fortawesome/free-solid-svg-icons";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import Tooltip from "./Tooltip.svelte";
  interface Props {
    versions: Versions;
  }

  let { versions }: Props = $props();

  const drawerStore = getDrawerStore();
  function openDrawer() {
    drawerStore.open({
      width: "max-w-[80%] w-96",
    });
  }
</script>

<AppBar
  gridColumns="grid-cols-3"
  slotDefault="place-self-center"
  slotTrail="place-content-end"
>
  {#snippet lead()}
    <button onclick={openDrawer}>
      <Fa icon={faBars} size="lg" />
    </button>
  {/snippet}

  <p class="text-xl text-center">
    <strong> PGFinder </strong>
    <Tooltip style="inline ml-1" width="w-44" type="info">
      <div class="grid grid-flow-row-dense text-sm text-left">
        {#each Object.entries(versions) as [tool, version]}
          <strong>{tool}:</strong>
          {#if version}
            <p class="col-start-2 font-mono ml-1">v{version}</p>
          {:else}
            <div class="placeholder animate-pulse"></div>
          {/if}
        {/each}
      </div>
    </Tooltip>
  </p>

  {#snippet trail()}
    <a
      href="https://pgfinder.readthedocs.io/en/latest/usage.html"
      target="_blank"
    >
      <Fa icon={faBook} size="lg" />
    </a>

    <a href="https://github.com/Mesnage-Org/pgfinder" target="_blank">
      <Fa icon={faGithub} size="lg" />
    </a>
  {/snippet}
</AppBar>

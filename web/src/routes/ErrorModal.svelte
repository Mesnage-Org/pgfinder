<script lang="ts">
  import { getModalStore } from "@skeletonlabs/skeleton";
  export let message: string;
  export let manualError: boolean;

  const modalStore = getModalStore();
  let traceVisible = false;

  $: userError =
    message.match("(?<=pgfinder.errors.UserError: ).*") ||
    (manualError && message);

  $: traceHidden = traceVisible || !userError ? "" : "hidden";
  $: modalWidth = traceHidden ? "w-modal-slim" : "w-full max-w-3xl";
</script>

<div class="card flex flex-col gap-4 {modalWidth} max-h-[80vh] transition-all">
  <header class="card-header">
    {#if userError}
      <h3 class="h3 text-center">Something Went Wrong</h3>
    {:else}
      <h3 class="h3 text-center">PGFinder Encountered an Error</h3>
    {/if}
  </header>
  <p class="mx-4">
    {#if userError}
      {userError}
    {:else}
      PGFinder encountered an internal error that we've not come across before.
      Please
      <a
        href="https://github.com/Mesnage-Org/pgfinder/issues/new?labels=bug&template=bug_report.md"
        class="anchor"
        target="_blank"
      >
        create a bug report
      </a> on GitHub and include the following error message:
    {/if}
  </p>
  <div
    class="{traceHidden} mx-4 overflow-auto shadow bg-neutral-900/90 text-xs text-error-500"
  >
    <pre class="p-4 pt-1"><code>{message}</code></pre>
  </div>
  <footer class="card-footer flex flex-row-reverse justify-between">
    <button
      type="button"
      class="btn variant-filled"
      on:click={() => modalStore.close()}>Okay</button
    >
    {#if userError && !manualError}
      <button
        type="button"
        class="btn variant-filled-error"
        on:click={() => (traceVisible = !traceVisible)}
      >
        {#if traceVisible}
          Hide
        {:else}
          Show
        {/if} Trace
      </button>
    {/if}
  </footer>
</div>

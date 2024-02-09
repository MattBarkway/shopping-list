<script lang="ts">
  import type { PageData } from "./$types";
  import { onMount } from "svelte";
  import { invalidateAll } from "$app/navigation";

  export let data: PageData;
  onMount(async () => {
    if (data.logged_out) {
      invalidateAll();
    }
  });
</script>
{#if data.logged_out}
  You've successfully logged out!
{:else }
  Whoops
{/if}

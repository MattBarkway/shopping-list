<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

</script>

{#if data.error}
  Failed to validate: {data.error}

{/if}

<style>

</style>

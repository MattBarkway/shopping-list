<script>
  import { page } from "$app/stores";

  export let data;
</script>

<svelte:head>
  <title>Login</title>
</svelte:head>

Welcome to list number { $page.params.listID }

<ul>
  {#each data.items as item}
    <li>{ item }</li>
  {/each}
</ul>

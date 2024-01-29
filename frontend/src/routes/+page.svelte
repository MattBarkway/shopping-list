<script lang="ts">
  import type { PageData } from "./$types";
  import WelcomePage from "../components/WelcomePage.svelte";
  import HomePage from "../components/HomePage.svelte";

  export let data: PageData;
</script>

<svelte:head>
  <title>Shopping Basket</title>
  <meta name="description" content="A collaborative shopping list!" />
</svelte:head>

{#if !data.lists}
  <WelcomePage />
{:else }
  <HomePage lists="{data.lists}" />
{/if}

<!--TODO:
- Handle editing/deleting list items
- Prevent duplicate list items
- Add collaborator functionality
- sign out function
- better auth approach http only cookies/ localstorage
-->

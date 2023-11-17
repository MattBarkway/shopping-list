<script>
  import ShoppingList from "../components/ShoppingList.svelte";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { isAuthenticated, logout } from "$lib/auth";
  import MyLists from "../components/MyLists.svelte";
  import { getLists } from "$lib/api";

  let authenticated = false;

  onMount(() => {
    authenticated = isAuthenticated();
    if (!authenticated) {
      goto("/login");
    }
  });

  let listPromise = getLists();

  async function handleLogout() {
    await logout();
    await goto("/login");
  }
</script>

<svelte:head>
  <title>Shopping Basket</title>
  <meta name="description" content="A collaborative shopping list!" />
</svelte:head>

<section>
  {#if authenticated}
    <button on:click={handleLogout}>Logout</button>
    {#await listPromise}
      loading...
    {:then lists}
      <MyLists lists="{lists}" />
    {:catch error}
      <p style="color: red">{error.message}</p>
    {/await}
    <!--    <ShoppingList />-->
  {/if}
</section>

<style>

</style>

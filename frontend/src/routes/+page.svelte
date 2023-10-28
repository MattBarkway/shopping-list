<script>
	import ShoppingList from "../components/ShoppingList.svelte";
	import { isAuthenticated, login, logout } from '../services/auth';
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";

	let authenticated = false;

	onMount(() => {
    authenticated = isAuthenticated();
  });


    async function handleLogin() {
        // Perform login logic here
        // If login is successful, navigate to another route
        await goto('/login'); // Example route to navigate to
    }

    async function handleRegistration() {
        // Perform registration logic here
        // If registration is successful, navigate to another route
        await goto('/register'); // Example route to navigate to
    }
</script>

<svelte:head>
	<title>Shopping Basket</title>
	<meta name="description" content="A collaborative shopping list!" />
</svelte:head>

<section>
	{#if authenticated}
    <!-- Render content for authenticated users -->
    <button on:click={handleRegistration}>Logout</button>
  {:else}
    <!-- Render content for non-authenticated users -->
    <button on:click={handleLogin}>Login</button>
  {/if}
	<ShoppingList />
</section>

<style>

</style>

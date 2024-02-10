<script lang="ts">
	import type { PageData } from './$types';
	import WelcomePage from '../components/WelcomePage.svelte';
	import HomePage from '../components/HomePage.svelte';
	import { onMount } from 'svelte';
	export let data: PageData;

	onMount(() => {
		// TODO show updates to any lists visible to user
		// subscribe to listIDs, receive notifications when any are updated
		// Or notify of update once user can rename/delete lists
    const ws = new WebSocket(`ws://localhost:8080/ws/test/0`);

    ws.onmessage = (event) => {
			console.log({event});
    };

    ws.onerror = (event) => {
      console.error('WebSocket error:', event);
    };
  });
</script>

<svelte:head>
	<title>Shopping Basket</title>
	<meta name="description" content="A collaborative shopping list!" />
</svelte:head>

{#if !data.lists}
	<WelcomePage />
{:else}
	<HomePage lists={data.lists} sharedLists={data.sharedLists} />
{/if}

<!--TODO:
- Prevent duplicate list items
-->

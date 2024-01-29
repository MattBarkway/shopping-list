<script lang="ts">
	import type { ActionData } from './$types';
	export let form: ActionData;
</script>

<svelte:head>
  <title>Create List</title>
</svelte:head>


<form method="POST">
	<label>
		Name
		<input name="name" type="text">
	</label>
	<button>Create</button>
</form>

{#if form?.success}
	<p>List Created!</p>
{/if}
{#if form?.error}
	<p>Cockup alert: {form?.error}</p>
{/if}

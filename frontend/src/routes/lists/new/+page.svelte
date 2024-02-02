<script lang="ts">
	import type { ActionData } from './$types';
	import List from "../../../components/List.svelte";
	import ListItem from "../../../components/ListItem.svelte";
	export let form: ActionData;
</script>

<svelte:head>
  <title>Create List</title>
</svelte:head>


<form method="POST">
  <List>
		<p>Create a new list:</p>
    <ListItem>
      <input class="text-box dark" name="name" type="text" placeholder="name">
    </ListItem>
    <button class="dark button">Create</button>
  </List>
</form>

{#if form?.error}
	<p class="error">Cockup alert: {form?.error}</p>
{/if}


<style>
    .dark {
        background: #252525;
        color: #ffffff;
    }

    .button {
        cursor: pointer;
        padding: 0.5em;
        border-radius: 0.5em;
        border: none;
    }

		    a {
        color: #dcdcdc;
    }

    .error {
        color: #ffafaf;
        font-weight: bold;
    }


    .text-box {
        margin-left: 1em;
        width: 90%;
        padding: 0.5em;
        border: none;
    }

    input:focus {
        outline: none;
        border: none;
    }
</style>

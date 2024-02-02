<script lang="ts">
  import { spring } from "svelte/motion";
  import ListSummary from "./ListSummary.svelte";
  import { goto } from "$app/navigation";

  let count = 43;
  export let lists: string[] = [];


  const displayed_count = spring();
  $: displayed_count.set(count);
  $: offset = modulo($displayed_count, 1);

  function modulo(n: number, m: number) {
    // handle negative numbers
    return ((n % m) + m) % m;
  }

  async function handleClick(event) {
    console.log("Clicked!");
    console.log(event);
    await goto(`/lists/${event.detail.listID}`);
  }

  async function handleCreateList() {

  }
</script>

<div class="shopping-list">
  Your Shopping Lists:
  {#if !!lists}
    {#each lists as list, i}
      <ListSummary on:click={handleClick} name="{list['name']}" totalItems="{list['item_count']}"
                   owner="{list['owner']}" listID="{list['id']}" />
    {/each}
  {:else}
    You don't have any lists
    <button on:click={handleCreateList}>Create a list</button>
  {/if}

</div>

<style>
    * {
        font-family: Helvetica, sans-serif;
    }

    .shopping-list {
        font-family: Helvetica, sans-serif;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        padding: 1rem;
        background: #444444;
        border-radius: 1em;
        opacity: 0.5;
        color: white;
    }
</style>

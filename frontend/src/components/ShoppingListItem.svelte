<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import ListItem from "./ListItem.svelte";
  import { onMount } from "svelte";

  export let id: string;
  export let name: string;
  export let quantity: string;
  $: edit = false;
  const dispatch = createEventDispatcher();

  let originalName: string;
  let originalQuantity: string;

  onMount(async () => {
    originalName = name;
    originalQuantity = quantity;
  });
  function editItem() {
    // TODO add a spinner while waiting
    if (name === originalName && quantity === originalQuantity) {
      edit = false;
      return;
    }
    dispatch("edit", {
      id, name, quantity
    });
    edit = false;
  }

  function deleteItem() {
    dispatch("delete", {
      id
    });
  }

  function activateEditMode() {
    edit = true;
  }
</script>

  {#if edit}
    <ListItem>
      <input class="item-text" name="name" type="text" bind:value="{name}"/>
      <input class="item-text narrow" name="quantity" type="text" bind:value="{quantity}">
      <button on:click={editItem} class="action">💾</button>
    </ListItem>
  {:else}
    <ListItem>
      <div class="item-text">{name}</div>
      <div class="item-text narrow">{quantity}</div>
      <button class="action" on:click={activateEditMode}> ✏️</button>
      <button class="action" on:click={deleteItem}> 🗑️️</button>
    </ListItem>
  {/if}


<style>
    .action {
        border: 1px solid #252525;
        border-radius: 1em;
        padding: 0.7em;
        margin: 0.3em;
        cursor: pointer;
        background: black
    }

    .action:hover {
        background-color: #131313;
        opacity: 0.6;
        transition: 0.3s;
    }

    .item-text {
        width: 100%;
        padding: 1em;
        border-radius: 1em;
        border: none;
        background: none;
        color: white;

    }
    .narrow {
        width: 10%;
    }
</style>

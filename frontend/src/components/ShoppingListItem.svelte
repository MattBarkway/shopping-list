<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import ListItem from "./ListItem.svelte";

  export let id: string;
  export let name: string;
  export let quantity: string;
  $: edit = false;
  const dispatch = createEventDispatcher();

  function editItem() {
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
      <input class="item-text" name="name" type="text" value="{name}"/>
      <input class="item-text" name="quantity" type="text" value="{quantity}">
      <button on:click={editItem}>💾</button>
    </ListItem>
  {:else}
    <ListItem>
      <div class="item-text">{name} - {quantity}</div>
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
    }

    .action:hover {
        background-color: #131313;
        opacity: 0.6;
        transition: 0.3s;
    }

    .item-text {
        width: 100%;
        padding: 1em;
    }
</style>

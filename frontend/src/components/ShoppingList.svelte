<script lang="ts">
  import ShoppingListItem from "./ShoppingListItem.svelte";
  import ItemAdder from "./ItemAdder.svelte";
  import PlaceholderItem from "./PlaceholderItem.svelte";
  import { createEventDispatcher } from "svelte";
  import List from "./List.svelte";


  interface Item {
    name: string,
    description: string,
    quantity: number,
  }

  export let items: Item[];

  const dispatch = createEventDispatcher();

  function handleItemEdit(event: any) {
    console.log("edit item event:", event.detail)
    dispatch("edit-item", event.detail);
  }

  function handleItemDelete(event: any) {
    console.log("delete item event:", event.detail)
    dispatch("delete-item", event.detail);
  }

</script>

<List>
  <ItemAdder/>
  {#each items as item, i}
    <ShoppingListItem
      id="item-{i}"
      name="{item.name}"
      quantity="{item.quantity.toString(10)}"
      on:edit={handleItemEdit}
      on:delete={handleItemDelete}
    />
  {:else}
    <PlaceholderItem message="No items yet!"/>
  {/each}
</List>

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

<script lang="ts">
  import ShoppingListItem from "./ShoppingListItem.svelte";
  import ItemAdder from "./ItemAdder.svelte";
  import PlaceholderItem from "./PlaceholderItem.svelte";
  import { createEventDispatcher } from "svelte";
  import List from "./List.svelte";

  interface Item {
    id: string,
    name: string,
    description: string,
    quantity: number,
  }

  export let items: Item[];

  const dispatch = createEventDispatcher();

  function handleItemEdit(event: any) {
    dispatch("edit-item", event.detail);
  }

  function handleItemDelete(event: any) {
    dispatch("delete-item", event.detail);
  }

</script>

<List>
  <ItemAdder />
  {#each items as item}
    <ShoppingListItem
      id="{item.id}"
      name="{item.name}"
      quantity="{item.quantity.toString(10)}"
      on:edit={handleItemEdit}
      on:delete={handleItemDelete}
    />
  {:else}
    <PlaceholderItem message="No items yet!" />
  {/each}
</List>